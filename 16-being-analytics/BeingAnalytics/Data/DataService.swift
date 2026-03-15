//
//  DataService.swift
//  BeingAnalytics
//
//  Created by Zachary Sturman on 9/1/23.
//

import Foundation
import CoreData

// MARK: Fetch
extension DataService {
    func fetchAllActionStates() -> [ActionState] {
        //print("Fetching all action states...")
        let fetchRequest: NSFetchRequest<ActionState> = ActionState.fetchRequest()
        
        do {
            return try dataController.viewContext.fetch(fetchRequest)
        } catch {
            print("Error fetching ActionStates: \(error)")
            print("Fetch complete: 0 action states found.")
            return []
        }
    }
    
    
    func fetchObjectByID<T: NSManagedObject>(by id: UUID, entityType: T.Type) -> T? {
        let fetchRequest: NSFetchRequest<T> = T.fetchRequest() as! NSFetchRequest<T>
        fetchRequest.predicate = NSPredicate(format: "id == %@", id as CVarArg)
        
        do {
            let results = try dataController.viewContext.fetch(fetchRequest)
            return results.first
        } catch {
            print("Error fetching object by ID: \(error)")
            return nil
        }
    }

    
    
    func fetchExecutionsByActionStateID(actionStateID: UUID) -> [Execution] {
        //print("Fetching executions by ActionState ID: \(actionStateID)")
        let fetchRequest: NSFetchRequest<Execution> = Execution.fetchRequest()
        
        // Use a keypath to access the id of the related ActionState
        fetchRequest.predicate = NSPredicate(format: "actionState.id == %@", actionStateID as CVarArg)
        
        do {
            let results = try dataController.viewContext.fetch(fetchRequest)
            //print("Fetch by ActionState ID complete: \(results.count) executions found.")
            return results
        } catch {
            print("Error fetching Executions by ActionState ID: \(error)")
            return []
        }
    }
    
}


// MARK: Save
extension DataService {
    func saveNewActionState(actionState: ActionState) -> Bool {
        do {
            try dataController.saveChanges(in: dataController.viewContext)
            NotificationCenter.default.post(name: .newActionStateSaved, object: nil)
            print("ActionState saved successfully.")
            return true
        } catch let error as NSError {
            print("Could not save. \(error), \(error.userInfo)")
            return false
        }
    }
    
    func saveNewExecution(execution: Execution) -> Bool {
        guard let executionID = execution.id else {
            print("Execution ID is nil. Skipping save.")
            return false
        }
        
        let request: NSFetchRequest<Execution> = Execution.fetchRequest()
        request.predicate = NSPredicate(format: "id == %@", executionID.uuidString)
        
        let existingExecutions: [Execution]?
        do {
            existingExecutions = try dataController.viewContext.fetch(request)
        } catch {
            print("Failed to fetch existing executions. Error: \(error)")
            return false
        }
        
        if let existing = existingExecutions, !existing.isEmpty {
            // Execution with the same ID already exists, don't save
            print("Execution with ID \(executionID) already exists. Skipping save.")
            return false
        }
        
        // Save the new execution
        dataController.viewContext.insert(execution)
        do {
            try dataController.viewContext.save()
            return true
        } catch {
            print("Failed to save execution. Error: \(error)")
            return false
        }
    }
}


// MARK: Convert to CoreData
extension DataService {
    func convertTempExecutionToCoreData(tempExecutionData: TempExecution) -> Execution {
        //print("Converting Temp Execution to Core Data")
        
        let context = DataController.shared.viewContext
        let executionEntity = NSEntityDescription.entity(forEntityName: "Execution", in: context)!
        
        let newExecution = Execution(entity: executionEntity, insertInto: context)
        newExecution.id = tempExecutionData.id
        newExecution.timestamp = tempExecutionData.timestamp
        
        let executionActionState = fetchObjectByID(by: tempExecutionData.actionStateID, entityType: ActionState.self)
        newExecution.actionState = executionActionState
        
        for tempInputExecution in tempExecutionData.inputExecutions {
            let inputExecutionEntity = NSEntityDescription.entity(forEntityName: tempInputExecution.inputExecutionEntityName.rawValue, in: context)!
            var newInputExecution: InputExecution? = nil
            
            if tempInputExecution.inputExecutionEntityName == .InputExecutionDatetime {
                newInputExecution = InputExecutionDatetime(entity: inputExecutionEntity, insertInto: context) as InputExecution
                (newInputExecution as! InputExecutionDatetime).outputValue = tempInputExecution.outputValueDatetime
            }
                
            if tempInputExecution.inputExecutionEntityName == .InputExecutionString {
                newInputExecution = InputExecutionString(entity: inputExecutionEntity, insertInto: context) as InputExecution
                (newInputExecution as! InputExecutionString).outputValue = tempInputExecution.outputValueString
            }
            
            
            if tempInputExecution.inputExecutionEntityName == .InputExecutionNumber {
                newInputExecution = InputExecutionNumber(entity: inputExecutionEntity, insertInto: context) as InputExecution
                (newInputExecution as! InputExecutionNumber).outputValue = tempInputExecution.outputValueNumber ?? 0.0
            }
            
            if tempInputExecution.inputExecutionEntityName == .InputExecutionLocation {
                newInputExecution = InputExecutionLocation(entity: inputExecutionEntity, insertInto: context) as InputExecution
                (newInputExecution as! InputExecutionLocation).latitude = tempInputExecution.latitude ?? 00000
                (newInputExecution as! InputExecutionLocation).longitude = tempInputExecution.longitude ?? 00000
            }
            
            if let executionInput = fetchObjectByID(by: tempInputExecution.inputID!, entityType: Input.self) {
                let executionOrder = executionInput.order
                let inputTitle = executionInput.title

                newInputExecution?.input = executionInput
                newInputExecution?.order = executionOrder
                newInputExecution?.inputTitle = inputTitle
                
                if let executionAsk = executionInput as? InputAskForText {
                    if executionAsk.promptBool == true {
                        newInputExecution?.inputPromptBool = executionAsk.promptBool
                        newInputExecution?.inputPromptString = executionAsk.promptString
                    }
                }
                if let executionAsk = executionInput as? InputAskForNumber {
                    if executionAsk.promptBool == true {
                        newInputExecution?.inputPromptBool = executionAsk.promptBool
                        newInputExecution?.inputPromptString = executionAsk.promptString
                    }
                }
                
                
            }
            
            // Setting common properties
            newInputExecution?.id = tempInputExecution.id
            newInputExecution?.outputType = tempInputExecution.outputType
            newInputExecution?.execution = newExecution
            
        }
        
        if let lastInputExecution = tempExecutionData.inputExecutions.last {
            switch lastInputExecution.inputExecutionEntityName {
                case .InputExecutionDatetime:
                    if let date = lastInputExecution.outputValueDatetime {
                        let dateFormatter = DateFormatter()
                        dateFormatter.dateFormat = "yyyy-MM-dd HH:mm:ss"
                        newExecution.outputValue = dateFormatter.string(from: date)
                    } else {
                        newExecution.outputValue = "Error recovering datetime"
                    }
                case .InputExecutionString:
                    newExecution.outputValue = lastInputExecution.outputValueString
                case .InputExecutionNumber:
                    newExecution.outputValue = String(lastInputExecution.outputValueNumber ?? 0)
                default:
                    break
            }
        }

        
        return newExecution
    }

}

// MARK: Delete
extension DataService {

    func deleteActionState(_ actionState: ActionState) {
        let context = dataController.viewContext
        context.delete(actionState)
        do {
            try context.save()
            NotificationCenter.default.post(name: .deletedActionState, object: nil)
        } catch let error {
            print("Error deleting ActionState: \(error)")
        }
    }

}

class DataService: ObservableObject {
    
    var dataController: DataController
    
    init(dataController: DataController = DataController.shared) {
        self.dataController = dataController
    }

//    // MARK: CONVERT TO TEMP DATA
//    func convertActionStateToTempActionState(actionState: ActionState) -> TempActionState? {
//        guard let id = actionState.id,
//                let dateCreated = actionState.dateCreated,
//                let dateUpdated = actionState.dateUpdated,
//                let title = actionState.title else {
//            print("Error: Unable to convert ActionState to TempData due to nil values.")
//            return nil
//        }
//        
//        var tempTriggers: [TempTrigger] = []
//        
//        for trigger in actionState.triggers ?? [] {
//            if let tempTrigger = convertTriggerToTempTrigger(trigger: trigger as! Trigger) {
//                tempTriggers.append(tempTrigger)
//            } else {
//                print("Temp trigger = nil")
//            }
//        }
//
//        
//        let tempExecutions = actionState.executions?.compactMap { execution in
//            return convertExecutionToTempExecution(execution: execution as! Execution)
//        } ?? []
//        
//        let tempActionState = TempActionState(id: id, dateCreated: dateCreated, dateUpdated: dateUpdated, title: title, isAction: actionState.isAction, triggers: tempTriggers, executions: tempExecutions)
//        //print("Conversion complete.")
//        return tempActionState
//    }
    
    
    
//    func convertTriggerToTempTrigger(trigger: Trigger) -> TempTrigger? {
//        guard let id = trigger.id,
//              let title = trigger.title,
//              let _ = trigger.triggerSystemImage,
//            let _ = trigger.triggerType
//        else {
//            print("Error: Unable to convert Trigger to Temp Data due to nil values")
//            return nil
//        }
//        
//        var tempInputs: [TempInput] = []
//        
//        for input in trigger.inputs ?? [] {
//            if let tempInput = convertInputToTempInput(input: input as! Input) {
//                tempInputs.append(tempInput)
//            }
//        }
//        
//        // Convert Execution to TempExecution
//        let tempExecutions = trigger.executions?.compactMap { execution in
//            return convertExecutionToTempExecution(execution: execution as! Execution)
//        } ?? []
//        
//        let firstInputID = tempInputs.first?.id
//        let lastInputID = tempInputs.last?.id
//        
//        return TempTrigger(id: id,
//                            title: title,
//                            firstInputID: firstInputID,
//                            lastInputID: lastInputID,
//                            inputs: tempInputs,
//                            executions: tempExecutions)
//    }
    
    
    
//    func convertInputToTempInput(input: Input) -> TempInput? {
//        //print("Starting conversion of Input to TempInput...")
//        
//        guard let id = input.id, let inputType = input.inputType else {
//            print("Error: Unable to convert Input to TempInput due to nil values.")
//            return nil
//        }
//        
//        guard let convertedInputType = InputTypeOptions(rawValue: inputType) else {
//            print("Error: Invalid inputType value.")
//            return nil
//        }
//        
//        let order = Int(input.order)
//        
//        var newTempInput = TempInput(id: id, inputType: convertedInputType, order: order)
//        
//        if let tempInput = input as? InputAskForText {
//            newTempInput.allowBlank = tempInput.allowBlank
//            newTempInput.defaultBool = tempInput.defaultBool
//            newTempInput.promptBool = tempInput.promptBool
//
//            if tempInput.defaultBool == true {
//                if let defaultStr = tempInput.defaultString {
//                    newTempInput.defaultString = defaultStr
//                } else {
//                    newTempInput.defaultString = ""
//                }
//            } else {
//                newTempInput.defaultString = ""
//            }
//
//            if tempInput.promptBool == true {
//                if let promptStr = tempInput.promptString {
//                    newTempInput.promptString = promptStr
//                } else {
//                    newTempInput.promptString = ""
//                }
//            } else {
//                newTempInput.promptString = ""
//            }
//        } else if let tempInput = input as? InputAskForNumber {
//            newTempInput.promptBool = tempInput.promptBool
//            
//            if tempInput.promptBool == true {
//                if let promptStr = tempInput.promptString {
//                    newTempInput.promptString = promptStr
//                } else {
//                    newTempInput.promptString = ""
//                }
//            } else {
//                newTempInput.promptString = ""
//            }
//            
//            newTempInput.allowDecimals = tempInput.allowDecimals
//            newTempInput.allowNegatives = tempInput.allowNegatives
//            newTempInput.currency = tempInput.currency
//            
//            newTempInput.useRange = tempInput.useRange
//            newTempInput.defaultNumberValue = tempInput.defaultValue
//            newTempInput.maxNumberValue = tempInput.maxValue
//            newTempInput.minNumberValue = tempInput.minValue
//            newTempInput.stepCount = tempInput.stepCount
//
//        } else if let tempInput = input as? InputSetText {
//            newTempInput.setValue = tempInput.setValue ?? ""
//        } else if let tempInput = input as? InputSetNumber {
//            newTempInput.currency = tempInput.currency
//            newTempInput.numberValue = tempInput.setValue
//        } else if let tempInput = input as? InputCurrentDatetime {
//            newTempInput.date = tempInput.date
//            newTempInput.time = tempInput.time
//        } else if let tempInput = input as? InputCalculate {
//            
//            
//            if tempInput.valueOneIsInput == true {
//                newTempInput.selectedInputOne = tempInput.selectedInputOne?.id
//                newTempInput.valueOne = 0
//            } else {
//                newTempInput.valueOne = tempInput.valueOne
//            }
//            
//            if tempInput.valueTwoIsInput == true {
//                newTempInput.selectedInputTwo = tempInput.selectedInputTwo?.id
//                newTempInput.valueTwo = 0
//            } else {
//                newTempInput.valueTwo = tempInput.valueTwo
//            }
//            
//
//            
//            if let calculationTypeString = tempInput.calculationType {
//                if let calcType = CalculationType(rawValue: calculationTypeString) {
//                    newTempInput.calculationType = calcType
//                } else {
//                    print("[DataService.swift - convertInputToTempInput]: String does not match any CalculationType enum's raw values: \(calculationTypeString)")
//                }
//            } else {
//                print("[DataService.swift - convertInputToTempInput]: tempInput.calculationType is nil")
//            }
//
//            // For calculationOutputType
//            if let calculationOutputTypeString = tempInput.calculationOutputType {
//                if let outputType = NumberType(rawValue: calculationOutputTypeString) {
//                    newTempInput.calculationOutputType = outputType
//                } else {
//                    print("[DataService.swift - convertInputToTempInput]: String does not match any NumberType enum's raw values: \(calculationOutputTypeString)")
//                }
//            } else {
//                print("[DataService.swift - convertInputToTempInput]: tempInput.calculationOutputType is nil")
//            }
//
//            // For calculationDateOrTime
//            if let calculationDateOrTimeString = tempInput.calculationDateOrTime {
//                if let dateOrTime = DateOrTime(rawValue: calculationDateOrTimeString) {
//                    newTempInput.calculationDateOrTime = dateOrTime
//                } else {
//                    print("[DataService.swift - convertInputToTempInput]: String does not match any DateOrTime enum's raw values: \(calculationDateOrTimeString)")
//                }
//            } else {
//                print("[DataService.swift - convertInputToTempInput]: tempInput.calculationDateOrTime is nil")
//            }
//
//            // For calculateOperation
//            if let calculateOperationString = tempInput.calculateOperation {
//                if let operation = Operation(rawValue: calculateOperationString) {
//                    newTempInput.calculateOperation = operation
//                } else {
//                    print("[DataService.swift - convertInputToTempInput]: String does not match any Operation enum's raw values: \(calculateOperationString)")
//                }
//            } else {
//                print("[DataService.swift - convertInputToTempInput]: tempInput.calculateOperation is nil")
//            }
//
//        }
//
//        return newTempInput
//    }
                    

    
    func convertExecutionToTempExecution(execution: Execution) -> TempExecution? {
        print("Converting Execution to TempData")
        
        guard let id = execution.id,
                let outputValue = execution.outputValue,
                let timestamp = execution.timestamp,
                let actionStateID = execution.actionState?.id else {
            print("Error: Unable to convert Execution to TempExecution due to nil values.")
            return nil
        }
        
        // Convert inputExecutions to TempInputExecution
        let tempInputExecutions = execution.inputExecutions?.compactMap { inputExecution in
            return convertInputExecutionToTempInputExecution(inputExecution: inputExecution as! InputExecution)
        } ?? []
        
        
        return TempExecution(id: id,
                                outputValue: outputValue,
                                timestamp: timestamp,
                                actionStateID: actionStateID,
                                inputExecutions: tempInputExecutions)
    }
    
    func convertInputExecutionToTempInputExecution(inputExecution: InputExecution) -> TempInputExecution? {
        print("Converting InputExecution to TempData")
        
        guard let id = inputExecution.id,
              let outputType = inputExecution.outputType else {
            print("Error: Unable to convert InputExecution to TempInputExecution due to nil values.")
            return nil
        }

        return TempInputExecution(id: id, outputType: outputType)
    }


}
