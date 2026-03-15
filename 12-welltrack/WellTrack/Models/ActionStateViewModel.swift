//
//  ActionStateViewModel.swift
//  WellTrack
//
//  Created by Zachary Sturman on 8/15/23.
//

import CoreData
import Foundation

final class ActionStateViewModel: ObservableObject {
    
    @Published var actionState: ActionState
    @Published var inputsArray: [Input] = []
    @Published var triggersArray: [Trigger] = []
    @Published var parentTrigger: Trigger?
    @Published var executionsArray: [ExecutionRecord] = []
    
    @Published var showingInputExecutionSheet: Bool = false
    @Published var currentExecutionItem: Input?
    
    let isNew: Bool
    private let controller: ActionStateDataController
    private let context: NSManagedObjectContext
    
    init(controller: ActionStateDataController, actionState: ActionState? = nil) {
        self.controller = controller
        self.context = controller.newContext
        
        if let actionState, let existingActionStateCopy = controller.exists(actionState, in: context) {
            self.actionState = existingActionStateCopy
            self.inputsArray = Array(existingActionStateCopy.inputs) as! [Input]
            self.triggersArray = Array(existingActionStateCopy.triggers) as! [Trigger]
            self.executionsArray = Array(existingActionStateCopy.executionRecords) as! [ExecutionRecord]
            self.isNew = false
            
        } else {
            self.actionState = ActionState(context: self.context)
            self.isNew = true
        }
    }


    func save() throws {
        actionState.inputs = NSSet(array: self.inputsArray)
        actionState.executionRecords = NSSet(array: self.executionsArray)
        actionState.triggers = NSSet(array: self.triggersArray)
        
        
        do {
            try controller.saveChanges(in: context)

        } catch let error as NSError {
            print("Could not save. \(error), \(error.userInfo)")
        }
    }

}

// INPUTS
extension ActionStateViewModel {
    
    func recomputeOrdering() {
        for index in 0..<inputsArray.count {
            let currentInput = inputsArray[index]

            let previousInput = index > 0 ? inputsArray[index - 1] : nil
            let nextInput = index < inputsArray.count - 1 ? inputsArray[index + 1] : nil

            currentInput.nextInput = nextInput
            currentInput.previousInput = previousInput
            currentInput.isFirst = (index == 0)
            currentInput.orderIndex = Int16(index)
        }
    }


    func addInput(inputs: [Input]) {
        for input in inputs {
            if !self.inputsArray.contains(where: { $0.id == input.id }) {
                self.inputsArray.append(input)
                input.orderIndex = Int16(self.inputsArray.count - 1) // Set orderIndex to its position
            }
        }
        actionState.inputs = NSSet(array: self.inputsArray)
        recomputeOrdering()
    }



    func removeInput(input: Input) {
        if let index = self.inputsArray.firstIndex(of: input) {
            self.inputsArray.remove(at: index)
            actionState.inputs = NSSet(array: self.inputsArray)
        }
        recomputeOrdering()
    }

    // You can also add a rearrangeInput function if necessary.
    func rearrangeInput(fromIndex: Int, toIndex: Int) {
        guard fromIndex != toIndex, fromIndex >= 0, toIndex >= 0, fromIndex < inputsArray.count, toIndex < inputsArray.count else {
            return
        }

        let movedItem = inputsArray.remove(at: fromIndex)
        inputsArray.insert(movedItem, at: toIndex)
        recomputeOrdering()
    }


    
    func addTrigger(triggers: [Trigger]) {
        print("Adding triggers. Current count: \(triggersArray.count). New triggers count: \(triggers.count)")
        
        self.triggersArray.append(contentsOf: triggers)
        
        print("Attempting to update actionState.triggers...")
        actionState.triggers = NSSet(array: self.triggersArray)
        print("Updated actionState.triggers successfully.")
        
        print("Updated triggers count: \(triggersArray.count)")
    }

    func askForTextInput() -> AskForTextInput {
        let newInput = controller.askForTextInput(in: self.context)
        newInput.title = "AskForTextInput \(inputsArray.count + 1)"
        newInput.parentTrigger = self.parentTrigger
        newInput.inputType = "AskForTextInput"
        newInput.outputValue = "Output Value here!"
        addInput(inputs: [newInput])
        return newInput
    }

    func askForNumberInput() -> AskForNumberInput {
        let newInput = controller.askForNumberInput(in: self.context)
        newInput.title = "AskForNumberInput Input \(inputsArray.count + 1)"
        newInput.parentTrigger = self.parentTrigger
        newInput.inputType = "AskForNumberInput"
        newInput.outputValue = 100
        addInput(inputs: [newInput])
        return newInput
    }
    
    func setTextInput() -> SetTextInput {
        let newInput = controller.setTextInput(in: self.context)
        newInput.title = "SetTextInput \(inputsArray.count + 1)"
        newInput.parentTrigger = self.parentTrigger
        newInput.inputType = "SetTextInput"
        newInput.outputValue = "This is output for Set Text"
        addInput(inputs: [newInput])
        return newInput
    }
    
    func setNumberInput() -> SetNumberInput {
        let newInput = controller.setNumberInput(in: self.context)
        newInput.title = "SetNumberInput \(inputsArray.count + 1)"
        newInput.parentTrigger = self.parentTrigger
        newInput.inputType = "SetNumberInput"
        newInput.outputValue = 500
        addInput(inputs: [newInput])
        return newInput
    }

    
    func calculateInput() -> CalculateInput {
        let newInput = controller.calculateInput(in: self.context)
        newInput.title = "CalculateInput \(inputsArray.count + 1)"
        newInput.parentTrigger = self.parentTrigger
        newInput.inputType = "CalculateInput"
        newInput.outputValue = 900
        addInput(inputs: [newInput])
        return newInput
    }
}

// TRIGGERS
extension ActionStateViewModel {

    func createButtonTrigger() -> TriggerButton {
        let newTrigger = controller.createTriggerButton(in: self.context)
        newTrigger.title = "Button trigger"
        newTrigger.systemImage = "play.circle.fill"
        newTrigger.buttonText = "X"
        
        if let childInputsSet = newTrigger.childInputs as? Set<Input>,
            !childInputsSet.isEmpty {
            for childInput in childInputsSet {
                childInput.isFirst = false
            }
            childInputsSet.first?.isFirst = true
        }


        addTrigger(triggers: [newTrigger])
        return newTrigger
    }
}

extension ActionStateViewModel {
    
    func addExecutionRecord(trigger: Trigger) {
        if let childInputsSet = trigger.childInputs as? Set<Input> {
            if let firstChildInput = childInputsSet.first(where: { $0.isFirst }) {
                // Make sure the firstChildInput has the matching Trigger item
                if firstChildInput.parentTrigger == trigger {
                    executeInput(input: firstChildInput)
                    
                    if let nextInput = firstChildInput.nextInput {
                        recursiveNextInput(input: nextInput)
                    }
                } else {
                    print("Error matching Inputs to Trigger")
                }
                
                do {
                    try self.context.save()
                } catch {
                    print("Error saving new execution record: \(error)")
                }
            } else {
                print("Error: No first input found for this trigger.")
            }
        }
    }
    
    func executeInput(input: Input) {
        currentExecutionItem = input
        showingInputExecutionSheet = true

        switch InputType(rawValue: input.inputType) {
        case .askForTextInput:
            if let textInput = input as? AskForTextInput {
                let newExecution = createExecutionString(from: textInput, context: self.context)
                self.actionState.addToExecutionRecords(newExecution)
            }
        case .askForNumberInput:
            if let numberInput = input as? AskForNumberInput {
                let newExecution = createExecutionNumber(from: numberInput, context: self.context)
                self.actionState.addToExecutionRecords(newExecution)
            }
        case .setTextInput, .setNumberInput, .calculationInput:
            // Handle these cases if required or print an appropriate message
            break
        case .none:
            // Handle the situation where the input type doesn't match any known values
            print("Error: Unknown input type.")
        }
    }
    
    public func recursiveNextInput(input: Input) {
        if !showingInputExecutionSheet, let nextItem = input.nextInput {
            executeInput(input: nextItem)
            recursiveNextInput(input: nextItem)
        }
    }



    

    private func createExecutionString(from input: AskForTextInput, context: NSManagedObjectContext) -> ExecutionString {
        print("Making new string")
        let newExecution = controller.executeStringOutput(in: self.context)
        newExecution.timestamp = Date()
        newExecution.outputValue = input.outputValue
        return newExecution
    }

    private func createExecutionNumber(from input: AskForNumberInput, context: NSManagedObjectContext) -> ExecutionNumber {
        print("Making new number")
        let newExecution = controller.executeNumberOutput(in: self.context)
        newExecution.timestamp = Date()
        newExecution.outputValue = input.outputValue
        return newExecution
    }

    
    var sortedExecutions: [ExecutionRecord] {
        let sortedArray = executionsArray.sorted(by: { $0.timestamp < $1.timestamp })
        return sortedArray
    }
}

