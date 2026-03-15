//
//  CreateActionStateVM.swift
//  BeingAnalytics
//
//  Created by Zachary Sturman on 9/1/23.
//

import Foundation
import CoreData

class CreateActionStateVM: ObservableObject {
    
    var dataService: DataService
    @Published var newActionState: TempActionState
    @Published var selectedTrigger: TempTrigger?
    var editingActionState: ActionState?
    
    @Published var errorMessage: String? = nil
    
    init(dataService: DataService, actionState: ActionState? = nil) {
        self.dataService = dataService
        self.editingActionState = actionState
        
        if let actionState = editingActionState {
            self.newActionState = TempActionState(from: actionState, in: dataService.dataController.viewContext)
            for var trigger in newActionState.triggers {
                print(trigger.title)
                
                reorderInputs(for: &trigger)
            }
        } else {
            self.newActionState = TempActionState()
        }
    }

    
    func isTriggerUsed(triggerType: TriggerTypeOptions) -> Bool {
        return newActionState.triggers.contains { $0.title == triggerType.triggerTypeName }
    }

    
    func addTriggerIfNotUsed(triggerType: TriggerTypeOptions) -> Bool {
        if !isTriggerUsed(triggerType: triggerType) {
            let newTrigger = TempTrigger(title: triggerType.triggerTypeName)
            newActionState.triggers.append(newTrigger)
            return true
        } else {
            return false
        }
    }

     
    func addTrigger(selectedTrigger: String) {
        let newTrigger = TempTrigger(title: selectedTrigger)
        newActionState.triggers.append(newTrigger)
    }
    
    func deleteTrigger(_ trigger: TempTrigger) {
        if let index = newActionState.triggers.firstIndex(where: { $0.id == trigger.id }) {
            newActionState.triggers.remove(at: index)
        }
    }
    
    func createNewInput(selectedInput: InputTypeOptions, tempCalculate: TempInput? = nil, order: Int) -> TempInput {
        switch selectedInput {
        case .askForText:
            return TempInput(inputType: .askForText, order: order)
        case .askForNumber:
            return TempInput(inputType: .askForNumber, order: order)
        case .currentDatetime:
            return TempInput(inputType: .currentDatetime, order: order)
        case .getLocation:
            return TempInput(inputType: .getLocation, order: order)
        case .setText:
            return TempInput(inputType: .setText, order: order)
        case .setNumber:
            return TempInput(inputType: .setNumber, order: order)
        case .calculate:
            return tempCalculate ?? TempInput(inputType: .calculate, order: order)
        }
    }

    func updateTriggerWithNewInput(trigger: inout TempTrigger, newInput: TempInput) {
        
        // Find the index of the trigger in newActionState.triggers
        if let index = newActionState.triggers.firstIndex(where: { $0.id == trigger.id }) {
            // Modify the trigger
            var updatedTrigger = newActionState.triggers[index]
            updatedTrigger.inputs.append(newInput)
            
            // Check if the newInput is the first input in the updatedTrigger.inputs list
            if updatedTrigger.inputs.first?.id == newInput.id {
                updatedTrigger.firstInputID = newInput.id
            }
            
            // Check if the newInput is the last input in the updatedTrigger.inputs list
            if updatedTrigger.inputs.last?.id == newInput.id {
                updatedTrigger.lastInputID = newInput.id
            }
            
            // Setting nextInput and previousInput for each input
            for idx in 0..<updatedTrigger.inputs.count {
                if idx > 0 {
                    updatedTrigger.inputs[idx].previousInput = updatedTrigger.inputs[idx - 1].id
                } else {
                    updatedTrigger.inputs[idx].previousInput = nil
                }

                if idx < updatedTrigger.inputs.count - 1 {
                    updatedTrigger.inputs[idx].nextInput = updatedTrigger.inputs[idx + 1].id
                } else {
                    updatedTrigger.inputs[idx].nextInput = nil
                }
            }
            
            // Update the order of each TempInput in updatedTrigger.inputs after the move
            for (newOrder, _) in updatedTrigger.inputs.enumerated() {
                updatedTrigger.inputs[newOrder].order = newOrder
            }

            if newInput.inputType == .getLocation {
                updatedTrigger.getLocation = true
            }
            newActionState.triggers[index] = updatedTrigger
            
        } else {
            print("updateTriggerWithNewInput - Failed to find trigger in newActionState.triggers")
        }
    }

    func addInput(selectedInput: InputTypeOptions, tempCalculate: TempInput? = nil) {
        guard var trigger = selectedTrigger else {
            print("addInput - Guard check failed: selectedTrigger is nil")
            return
        }
        
        let order = trigger.inputs.count
        var newInput = createNewInput(selectedInput: selectedInput, tempCalculate: tempCalculate, order: order)
        
        if selectedInput == .calculate {
            handleCalculateInput(trigger: &trigger, calculateInput: &newInput)
        }
        
        updateTriggerWithNewInput(trigger: &trigger, newInput: newInput)
    }



    


    
    func deleteInput(from trigger: TempTrigger, inputID: UUID) {
        if let index = newActionState.triggers.firstIndex(where: { $0.id == trigger.id }) {
            var updatedTrigger = newActionState.triggers[index]
            
            if let inputIndex = updatedTrigger.inputs.firstIndex(where: { $0.id == inputID }) {
                let deletedInputType = updatedTrigger.inputs[inputIndex].inputType
                updatedTrigger.inputs.remove(at: inputIndex)
                
                // Reorder the inputs after deletion
                reorderInputs(for: &updatedTrigger)

                // Check if the deleted input was of type getLocation
                if deletedInputType == .getLocation {
                    if !updatedTrigger.inputs.contains(where: { $0.inputType == .getLocation }) {
                        updatedTrigger.getLocation = false
                    }
                }

                newActionState.triggers[index] = updatedTrigger
            }
        }
    }



    func moveInput(in trigger: TempTrigger, from source: IndexSet, to destination: Int) {
        if let index = newActionState.triggers.firstIndex(where: { $0.id == trigger.id }) {
            var updatedTrigger = newActionState.triggers[index]
            updatedTrigger.inputs.move(fromOffsets: source, toOffset: destination)
            
            // Reorder the inputs after moving
            reorderInputs(for: &updatedTrigger)
            
            newActionState.triggers[index] = updatedTrigger
        }
    }

    func reorderInputs(for trigger: inout TempTrigger) {
        var calculationInInputs: Bool = false
        var calculationInputs: [TempInput] = []
        
        for (index, input) in trigger.inputs.enumerated() {
            trigger.inputs[index].order = index
            
            if index == 0 {
                trigger.firstInputID = input.id
                print("First Input ID: \(input.id)")
            }
            
            if index == trigger.inputs.count - 1 {
                trigger.lastInputID = input.id
                print("Last Input ID: \(input.id)")
            }
            
            if index > 0 {
                trigger.inputs[index].previousInput = trigger.inputs[index - 1].id
            } else {
                trigger.inputs[index].previousInput = nil
            }

            if index < trigger.inputs.count - 1 {
                trigger.inputs[index].nextInput = trigger.inputs[index + 1].id
            } else {
                trigger.inputs[index].nextInput = nil
            }
            
            
            if input.inputType == .calculate {
                calculationInInputs = true
                calculationInputs.append(input)
            }
        }
        
        
        self.selectedTrigger = trigger
        if calculationInInputs == true {
            for var input in calculationInputs {
                handleCalculateInput(trigger: &trigger, calculateInput: &input)
            }
        }
    }
    
    
    func handleCalculateInput(trigger: inout TempTrigger, calculateInput: inout TempInput) {
        
        guard var calculationInput = trigger.inputs.first(where: { $0.id == calculateInput.id }) else {
            print("Can't find input for calculation")
            _ = calculateInput
            return
        }
        
        if calculationInput.valueOneIsInput {
            if let selectedInputOne = trigger.inputs.first(where: { $0.id == calculationInput.selectedInputOne}) {
                if selectedInputOne.inputType == .setNumber {
                    calculateInput.valueOne = selectedInputOne.numberValue
                }
                
                if selectedInputOne.order >= calculationInput.order {
                    calculationInput.selectedInputOne = nil
                }
            } else {
                calculationInput.selectedInputOne = nil
            }
        } else {
            if calculationInput.valueOne == nil {
                calculationInput.valueOne = 0
            }
        }
        
        if calculationInput.valueTwoIsInput {
            if let selectedInputTwo = trigger.inputs.first(where: { $0.id == calculationInput.selectedInputTwo}) {
                if selectedInputTwo.order >= calculationInput.order {
                    calculationInput.selectedInputTwo = nil
                }
            } else {
                calculationInput.selectedInputTwo = nil
            }
        } else {
            if calculationInput.valueTwo == nil {
                calculationInput.valueTwo = 0
            }
        }
        
        if let index = trigger.inputs.firstIndex(where: { $0.id == calculateInput.id }) {
                trigger.inputs[index] = calculationInput
            }
        
        if calculateInput.selectedInputOne != nil {
            if let selectedValueOne = trigger.inputs.first(where: { $0.id == calculateInput.selectedInputOne }) {
                if selectedValueOne.inputType == .setNumber {
                    calculateInput.valueOne = selectedValueOne.numberValue
                }
            }
            
        }
    }
    
    func updateCalculationValues(for input: TempInput) -> TempInput {
        var updatedInput = input

        if input.valueOneIsInput, let selectedInputOne = selectedTrigger?.inputs.first(where: { $0.id == input.selectedInputOne }) {
            if selectedInputOne.inputType == .setNumber ||  selectedInputOne.inputType == .askForNumber || selectedInputOne.inputType == .calculate {
                updatedInput.valueOne = selectedInputOne.numberValue
            } else {
                print("CreateActionStateVM.updateCalculationValues -- Unknown Type")
            }
        }

        if input.valueTwoIsInput, let selectedInputTwo = selectedTrigger?.inputs.first(where: { $0.id == input.selectedInputTwo }) {
            if selectedInputTwo.inputType == .setNumber ||  selectedInputTwo.inputType == .askForNumber || selectedInputTwo.inputType == .calculate {
                updatedInput.valueTwo = selectedInputTwo.numberValue
            } else {
                print("CreateActionStateVM.updateCalculationValues -- Unknown Type")
            }
        }
        
        runCalculations(input: &updatedInput)

        return updatedInput
    }
    
    func runCalculations(input: inout TempInput) {
        
        if input.inputType == .calculate {
            if input.calculationType == .number {
                let valueOne = input.valueOne ?? 10
                let valueTwo = input.valueTwo ?? 20
                
                switch input.calculateOperation {
                case .addition:
                    input.numberValue = valueOne + valueTwo
                case .subtraction:
                    input.numberValue = valueOne - valueTwo
                case .multiplication:
                    input.numberValue = valueOne * valueTwo
                case .division:
                    if valueTwo != 0 {
                        input.numberValue = valueOne / valueTwo
                    } else {
                        input.numberValue = 0
                    }
                }

                // Round to nearest cent if currency is selected
                if input.calculationOutputType == .currency {
                    input.numberValue = (input.numberValue * 100).rounded() / 100
                }
            }
        }
        
    }
    
    func updateTriggerOutputs(for trigger: TempTrigger) -> TempTrigger {
        var updatedTrigger = trigger
        
        // Logic to update triggerOutputDate
        // updatedTrigger.triggerOutputDate = ...

        // Logic to update triggerOutputLocation if trigger.getLocation == true
        // updatedTrigger.triggerOutputLocation = ...

        // Logic to update inputOutput of the last input
        // updatedTrigger.inputs.last?.inputOutput = ...
        
        return updatedTrigger
    }
    
    func updateTriggerValue(for triggerID: UUID, newValue: Double) {
        if let index = self.newActionState.triggers.firstIndex(where: { $0.id == triggerID }) {
           print("CreateActionStateVM - updateTriggerValue -- fix this so it will actually update calculate functions and Trigger output")
        }
    }




    @discardableResult
    func saveNewActionState() -> Bool {
        print("saveNewActionState called") // Debug print
        
        guard validActionStateName() else {
            print("validActionStateName failed") // Debug print
            errorMessage = "ActionState must have a title"
            return false
        }
        
        guard areAllTriggersValid() else {
            print("areAllTriggersValid failed") // Debug print
            return false
        }

        var saveSuccessful = false
        
        let context = dataService.dataController.viewContext
        
        if let existingActionState = editingActionState {
            print("Updating existing ActionState") // Debug print
            existingActionState.update(from: newActionState, in: context)
            
            // Save the context
            do {
                try context.save()
                saveSuccessful = true
            } catch {
                print("Error updating existing ActionState: \(error.localizedDescription)") // Debug print
                errorMessage = "Failed to update the ActionState."
                saveSuccessful = false
            }
        } else {
            print("Saving new ActionState") // Debug print
            // Use the convenience initializer to create a new ActionState
            let _ = ActionState(from: newActionState, in: context)
            
            do {
                print("newActionState details: \(newActionState)") // Print the details of newActionState

                try context.save()
                NotificationCenter.default.post(name: .actionStateUpdated, object: nil)
                saveSuccessful = true
            } catch {
                print("Error saving new ActionState: \(error)") // P
                print("Error updating ActionState: \(error.localizedDescription)")
                errorMessage = "Failed to save new ActionState."
                saveSuccessful = false
            }
        }
        
        if saveSuccessful {
            if let _ = editingActionState {
                // Post notification for updating an existing ActionState
                NotificationCenter.default.post(name: .actionStateUpdated, object: nil)
            } else {
                // Post notification for saving a new ActionState
                NotificationCenter.default.post(name: .newActionStateSaved, object: nil)
            }
        }
        
        return saveSuccessful
    }
    




    
    func validActionStateName() -> Bool {
        print("validActionStateName called") // Debug print
        if newActionState.title.isEmpty {
            return false
        }
        return true
    }


    func areAllTriggersValid() -> Bool {
        for trigger in newActionState.triggers {
            if trigger.inputs.isEmpty {
                errorMessage = "All triggers must have at least one input."
                return false
            }
            
            for input in trigger.inputs {
                switch input.inputType {
                case .askForNumber:
                    return validateInputAskForNumber(trigger: trigger, input: input)
                case .askForText:
                    return true
                case .calculate:
                    return validateInputCalculate(trigger: trigger, input: input)
                case .currentDatetime:
                    return true
                case .getLocation:
                    return true
                case .setNumber:
                    return true
                case .setText:
                    return true
                }
            }
        }
        return true
    }
    
    func validateInputCalculate(trigger: TempTrigger, input: TempInput) -> Bool {
        if input.valueOneIsInput == true && input.selectedInputOne == nil {
            errorMessage = "Unexpected error in calculation input in \(trigger.title) at \(input.order). Please remove the input and try again."
            return false
        }
        
        if input.valueTwoIsInput == true && input.selectedInputTwo == nil {
            errorMessage = "Unexpected error in calculation input in \(trigger.title) at \(input.order). Please remove the input and try again."
            return false
        }
        return true
    }
    
    
    func validateInputAskForNumber(trigger: TempTrigger, input: TempInput) -> Bool {
        print("validateInputAskForNumber called for trigger: \(trigger.title) and input order: \(input.order)") // Debug print
        if input.minNumberValue >= input.maxNumberValue {
            errorMessage = "In \(trigger.title) at \(input.order): When using range the minimum value cannot be the same or higher than the maximum value."
            return false
        }
        
        if input.stepCount >= (input.maxNumberValue - input.minNumberValue) {
            errorMessage = "In \(trigger.title) at \(input.order): When using range the step count value cannot be the same or higher than the difference of the minimum value and maximum value."
            return false
        }
        
        return true
    }


    
    
}
