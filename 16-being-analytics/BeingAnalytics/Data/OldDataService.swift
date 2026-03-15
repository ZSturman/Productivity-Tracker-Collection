//
//  OldDataService.swift
//  BeingAnalytics
//
//  Created by Zachary Sturman on 9/24/23.
//

import Foundation


//
//// MARK: Updates
//extension DataService {
//    func updateActionState(from tempActionState: TempActionState, to actionState: ActionState) -> Bool {
//        let context = DataController.shared.viewContext
//
//        // Update basic properties of the ActionState
//        actionState.id = tempActionState.id
//        actionState.dateUpdated = Date()  // Update the modification date
//        actionState.dateCreated = tempActionState.dateCreated
//        actionState.isAction = tempActionState.isAction
//        actionState.title = tempActionState.title
//
//        // Get a set of all current trigger IDs for the actionState
//        let currentTriggerIDs = Set(actionState.triggers?.map { ($0 as? Trigger)?.id }.filter { $0 != nil } as? [UUID] ?? [])
//
//
//        // Update or create triggers
//        for tempTrigger in tempActionState.triggers {
//
//            // Try to find the existing trigger
//            if let existingTrigger = actionState.triggers?.first(where: { ($0 as? Trigger)?.id == tempTrigger.id }) as? Trigger {
//                print("DataService.updateActionState: existingTrigger: \(existingTrigger.title ?? "Unknown trigger title")")
//                existingTrigger.title = tempTrigger.title
//                existingTrigger.triggerType = tempTrigger.triggerType.rawValue
//                existingTrigger.triggerSystemImage = tempTrigger.triggerSystemImage
//
//                let currentInputIDs = Set(existingTrigger.inputs?.map { ($0 as? Input)?.id }.filter { $0 != nil } as? [UUID] ?? [])
//
//                var previousInput: Input? = nil
//                for tempInput in tempTrigger.inputs {
//                    if let existingInput = existingTrigger.inputs?.first(where: { ($0 as? Input)?.id == tempInput.id }) as? Input {
//                        print("DataService.updateActionState: existingInput: \(existingInput.title ?? "Unknown input title")")
//                        existingTrigger.title = tempTrigger.title
//                        existingInput.id = tempInput.id
//                        existingInput.title = tempInput.title
//                        let orderInt32: Int32 = Int32(tempInput.order)
//                        existingInput.order = orderInt32
//                        existingInput.inputType = tempInput.inputType.rawValue
//                        existingInput.userActionRequired = tempInput.userActionRequired
//                        existingInput.trigger = existingTrigger
//                        existingInput.actionState = actionState
//                        existingInput.previousInput = previousInput
//
//                        if previousInput != nil {
//                            previousInput?.nextInput = existingInput
//                        }
//
//                        if tempInput.nextInput != nil {
//                            previousInput = existingInput
//                        } else {
//                            previousInput = nil
//                        }
//
//
//                        if let existingInputType = existingInput as? InputAskForText {
//                            existingInputType.allowBlank = tempInput.allowBlank
//                            existingInputType.defaultBool = tempInput.defaultBool
//                            existingInputType.defaultString = tempInput.defaultString
//                            existingInputType.promptBool = tempInput.promptBool
//                            existingInputType.promptString = tempInput.promptString
//
//                        } else if let existingInputType = existingInput as? InputAskForNumber {
//                                existingInputType.allowDecimals = tempInput.allowDecimals
//                                existingInputType.allowNegatives = tempInput.allowNegatives
//                                existingInputType.currency = tempInput.currency
//                                existingInputType.promptBool = tempInput.promptBool
//                                existingInputType.promptString = tempInput.promptString
//
//                                existingInputType.useRange = tempInput.useRange
//                                existingInputType.defaultValue = tempInput.defaultNumberValue
//                                existingInputType.maxValue = tempInput.maxNumberValue
//                                existingInputType.minValue = tempInput.minNumberValue
//                                existingInputType.stepCount = tempInput.stepCount
//
//                        } else if let existingInputType = existingInput as? InputSetText {
//                            existingInputType.setValue = tempInput.setValue
//
//
//                        } else if let existingInputType = existingInput as? InputSetNumber {
//                            existingInputType.currency = tempInput.currency
//                            existingInputType.setValue = tempInput.numberValue
//
//
//                        } else if let _ = existingInput as? InputGetLocation {
//
//                        } else if let existingInputType = existingInput as? InputCurrentDatetime {
//                            existingInputType.date = tempInput.date
//                            existingInputType.time = tempInput.time
//                        } else if let existingInputType = existingInput as? InputCalculate {
//                            existingInputType.valueOneIsInput = tempInput.valueOneIsInput
//                            if tempInput.valueOneIsInput == true {
//                                if let selectedInputOneID = tempInput.selectedInputOne {
//                                    let selectedInputOne = fetchObjectByID(by: selectedInputOneID, entityType: Input.self)
//                                    existingInputType.selectedInputOne = selectedInputOne
//                                } else {
//                                    print("Error get selectedInputOne from tempInput")
//                                    existingInputType.valueOne = tempInput.valueOne ?? 0
//                                }
//                            } else {
//                                existingInputType.valueOne = tempInput.valueOne ?? 0
//                            }
//
//                            existingInputType.valueTwoIsInput = tempInput.valueTwoIsInput
//                            if tempInput.valueTwoIsInput == true {
//                                if let selectedInputTwoID = tempInput.selectedInputTwo {
//                                    let selectedInputTwo = fetchObjectByID(by: selectedInputTwoID, entityType: Input.self)
//                                    existingInputType.selectedInputTwo = selectedInputTwo
//                                } else {
//                                    print("Error get selectedInputTwo from tempInput")
//                                    existingInputType.valueTwo = tempInput.valueTwo ?? 0
//                                }
//                            } else {
//                                existingInputType.valueTwo = tempInput.valueTwo ?? 0
//                            }
//
//                            existingInputType.calculateOperation = tempInput.calculateOperation.rawValue
//                            existingInputType.calculationDateOrTime = tempInput.calculationDateOrTime.rawValue
//                            existingInputType.calculationOutputType = tempInput.calculationOutputType.rawValue
//                            existingInputType.calculationType = tempInput.calculationType.rawValue
//
//                        }
//
//                    } else {
//                        print("DataService.updateActionState: NOT and existing input. Running createInput function: ")
//                        let newInput = createInput(from: tempInput, for: existingTrigger, actionState: actionState, with: &previousInput, in: context)
//
//                        print("DataService.updateActionState: new input title: \(newInput?.title ?? "Unknown input Title") ")
//
//                    }
//                }
//
//                // After iterating through tempTrigger.inputs for this trigger, determine which inputs have been deleted:
//                let deletedInputIDs = currentInputIDs.subtracting(tempTrigger.inputs.map { $0.id })
//
//                // Now delete these inputs from Core Data
//                for inputID in deletedInputIDs {
//                    if let inputToDelete = existingTrigger.inputs?.first(where: { ($0 as? Input)?.id == inputID }) as? Input {
//                        print("Input to delete: \(inputToDelete.order):\(inputToDelete.title ?? "Unknown input title")")
//                        context.delete(inputToDelete)
//                    }
//                }
//
//                existingTrigger.triggerOutput = tempTrigger.triggerOutput
//                existingTrigger.lastInputID = tempTrigger.lastInputID
//                existingTrigger.firstInputID = tempTrigger.firstInputID
//
//            } else {
//                print("DataService.updateActionState: NOT and existing trigger. Running createInput function: ")
//                let newTrigger = createTrigger(from: tempTrigger, for: actionState, in: context)
//
//                var previousInput: Input? = nil
//                for tempInput in tempTrigger.inputs {
//                    let newInput = createInput(from: tempInput, for: newTrigger, actionState: actionState, with: &previousInput, in: context)
//                    print("DataService.updateActionState: new input title: \(newInput?.title ?? "Unknown input Title") ")
//                }
//
//                print("DataService.updateActionState: new trigger title: \(newTrigger.title ?? "Unknown trigger Title") ")
//            }
//        }
//
//
//        // After iterating through tempActionState.triggers, determine which triggers have been deleted:
//        let deletedTriggerIDs = currentTriggerIDs.subtracting(tempActionState.triggers.map { $0.id })
//
//        // Now delete these triggers from Core Data
//        for triggerID in deletedTriggerIDs {
//            if let triggerToDelete = actionState.triggers?.first(where: { ($0 as? Trigger)?.id == triggerID }) as? Trigger {
//                print("Trigger to delete: \(triggerToDelete.title ?? "Unknown input title")")
//                context.delete(triggerToDelete)
//            }
//        }
//
//        do {
//            try dataController.viewContext.save()
//            NotificationCenter.default.post(name: .actionStateUpdated, object: nil)
//            return true
//        } catch {
//            print("Error updating ActionState: \(error.localizedDescription)")
//            return false
//        }
//    }
//}
//

//extension DataService {
//
//    func convertTempActionStateToCoreData(tempActionState: TempActionState) -> ActionState {
//        let context = DataController.shared.viewContext
//        let newActionState = createActionState(from: tempActionState, in: context)
//
//        for tempTrigger in tempActionState.triggers {
//            let newTrigger = createTrigger(from: tempTrigger, for: newActionState, in: context)
//
//            var previousInput: Input? = nil
//            for tempInput in tempTrigger.inputs {
//                _ = createInput(from: tempInput, for: newTrigger, actionState: newActionState, with: &previousInput, in: context)
//
//            }
//        }
//        return newActionState
//    }
//}


//extension DataService {
//
//    func createActionState(from tempActionState: TempActionState, in context: NSManagedObjectContext) -> ActionState {
//        let actionStateEntity = NSEntityDescription.entity(forEntityName: "ActionState", in: context)!
//        let newActionState = ActionState(entity: actionStateEntity, insertInto: context)
//
//        newActionState.id = tempActionState.id
//        newActionState.dateCreated = tempActionState.dateCreated
//        newActionState.dateUpdated = Date()
//        newActionState.isAction = tempActionState.isAction
//        newActionState.title = tempActionState.title
//
//        return newActionState
//    }
//}


//// MARK: Create Trigger
//extension DataService {
//    func createTrigger(from tempTrigger: TempTrigger, for actionState: ActionState, in context: NSManagedObjectContext) -> Trigger {
//        let triggerEntity = NSEntityDescription.entity(forEntityName: "Trigger", in: context)!
//        let newTrigger = Trigger(entity: triggerEntity, insertInto: context)
//        newTrigger.id = tempTrigger.id
//        newTrigger.title = tempTrigger.title
//        newTrigger.triggerType = tempTrigger.triggerType.rawValue
//        newTrigger.triggerSystemImage = tempTrigger.triggerSystemImage
//        newTrigger.triggerOutput = tempTrigger.triggerOutput
//        newTrigger.lastInputID = tempTrigger.lastInputID
//        newTrigger.firstInputID = tempTrigger.firstInputID
//        newTrigger.actionState = actionState
//        return newTrigger
//    }
//}

//
//// MARK: Create Input
//extension DataService {
//
//    func createInput(from tempInput: TempInput, for trigger: Trigger, actionState: ActionState, with previousInput: inout Input?, in context: NSManagedObjectContext) -> Input? {
//
//        var newInput: Input?
//
//
//        switch tempInput.inputType {
//        case .askForText:
//            let inputEntity = NSEntityDescription.entity(forEntityName: "InputAskForText", in: context)!
//            let newInput = InputAskForText(entity: inputEntity, insertInto: context)
//            newInput.id = tempInput.id
//            newInput.title = tempInput.title
//            let orderInt32: Int32 = Int32(tempInput.order)
//            newInput.order = orderInt32
//            newInput.inputType = tempInput.inputType.rawValue
//            newInput.userActionRequired = tempInput.userActionRequired
//
//
//            newInput.allowBlank = tempInput.allowBlank
//            newInput.defaultBool = tempInput.defaultBool
//            newInput.defaultString = tempInput.defaultString
//            newInput.promptBool = tempInput.promptBool
//            newInput.promptString = tempInput.promptString
//
//
//            newInput.trigger = trigger
//            newInput.actionState = actionState
//
//            newInput.previousInput = previousInput
//
//            if previousInput != nil {
//                previousInput?.nextInput = newInput
//            }
//
//            if tempInput.nextInput != nil {
//                previousInput = newInput
//            } else {
//                previousInput = nil
//            }
//        case .askForNumber:
//            let inputEntity = NSEntityDescription.entity(forEntityName: "InputAskForNumber", in: context)!
//            var newInput = InputAskForNumber(entity: inputEntity, insertInto: context)
//
//            //inputAskForNumber(newInput: &newInput, tempInput: tempInput)
//
//            newInput.trigger = trigger
//            newInput.actionState = actionState
//
//            newInput.previousInput = previousInput
//
//            if previousInput != nil {
//                previousInput?.nextInput = newInput
//            }
//
//            if tempInput.nextInput != nil {
//                previousInput = newInput
//            } else {
//                previousInput = nil
//            }
//
//
//
//            print(newInput)
//
//        case .setText:
//            let inputEntity = NSEntityDescription.entity(forEntityName: "InputSetText", in: context)!
//            let newInput = InputSetText(entity: inputEntity, insertInto: context)
//            newInput.id = tempInput.id
//            newInput.title = tempInput.title
//            let orderInt32: Int32 = Int32(tempInput.order)
//            newInput.order = orderInt32
//            newInput.inputType = tempInput.inputType.rawValue
//            newInput.userActionRequired = tempInput.userActionRequired
//
//            newInput.setValue = tempInput.setValue
//            newInput.trigger = trigger
//            newInput.actionState = actionState
//
//            newInput.previousInput = previousInput
//
//            if previousInput != nil {
//                previousInput?.nextInput = newInput
//            }
//
//            if tempInput.nextInput != nil {
//                previousInput = newInput
//            } else {
//                previousInput = nil
//            }
//
//        case .setNumber:
//
//            let inputEntity = NSEntityDescription.entity(forEntityName: "InputSetNumber", in: context)!
//            let newInput = InputSetNumber(entity: inputEntity, insertInto: context)
//            newInput.id = tempInput.id
//            newInput.title = tempInput.title
//            let orderInt32: Int32 = Int32(tempInput.order)
//            newInput.order = orderInt32
//            newInput.inputType = tempInput.inputType.rawValue
//            newInput.userActionRequired = tempInput.userActionRequired
//
//            newInput.currency = tempInput.currency
//            newInput.setValue = tempInput.numberValue
//            newInput.trigger = trigger
//            newInput.actionState = actionState
//
//            newInput.previousInput = previousInput
//
//            if previousInput != nil {
//                previousInput?.nextInput = newInput
//            }
//
//            if tempInput.nextInput != nil {
//                previousInput = newInput
//            } else {
//                previousInput = nil
//            }
//
//        case .getLocation:
//            let inputEntity = NSEntityDescription.entity(forEntityName: "InputGetLocation", in: context)!
//            let newInput = InputGetLocation(entity: inputEntity, insertInto: context)
//            newInput.id = tempInput.id
//            newInput.title = tempInput.title
//            let orderInt32: Int32 = Int32(tempInput.order)
//            newInput.order = orderInt32
//            newInput.inputType = tempInput.inputType.rawValue
//            newInput.userActionRequired = tempInput.userActionRequired
//
//            newInput.trigger = trigger
//            newInput.actionState = actionState
//
//            newInput.previousInput = previousInput
//
//            if previousInput != nil {
//                previousInput?.nextInput = newInput
//            }
//
//            if tempInput.nextInput != nil {
//                previousInput = newInput
//            } else {
//                previousInput = nil
//            }
//
//        case .currentDatetime:
//            let inputEntity = NSEntityDescription.entity(forEntityName: "InputCurrentDatetime", in: context)!
//            let newInput = InputCurrentDatetime(entity: inputEntity, insertInto: context)
//            newInput.id = tempInput.id
//            newInput.title = tempInput.title
//            let orderInt32: Int32 = Int32(tempInput.order)
//            newInput.order = orderInt32
//            newInput.inputType = tempInput.inputType.rawValue
//            newInput.userActionRequired = tempInput.userActionRequired
//
//
//            newInput.trigger = trigger
//            newInput.actionState = actionState
//            newInput.date = tempInput.date
//            newInput.time = tempInput.time
//
//            newInput.previousInput = previousInput
//
//            if previousInput != nil {
//                previousInput?.nextInput = newInput
//            }
//
//            if tempInput.nextInput != nil {
//                previousInput = newInput
//            } else {
//                previousInput = nil
//            }
//
//        case .calculate:
//            let inputEntity = NSEntityDescription.entity(forEntityName: "InputCalculate", in: context)!
//            let newInput = InputCalculate(entity: inputEntity, insertInto: context)
//            newInput.id = tempInput.id
//            newInput.title = tempInput.title
//            let orderInt32: Int32 = Int32(tempInput.order)
//            newInput.order = orderInt32
//            newInput.inputType = tempInput.inputType.rawValue
//            newInput.userActionRequired = tempInput.userActionRequired
//
//            newInput.trigger = trigger
//            newInput.actionState = actionState
//
//            newInput.calculateOperation = tempInput.calculateOperation.rawValue
//            newInput.calculationDateOrTime = tempInput.calculationDateOrTime.rawValue
//            newInput.calculationOutputType = tempInput.calculationOutputType.rawValue
//            newInput.calculationType = tempInput.calculationType.rawValue
//
//            newInput.valueOneIsInput = tempInput.valueOneIsInput
//            newInput.valueTwoIsInput = tempInput.valueTwoIsInput
//
//            if tempInput.valueOneIsInput == true {
//                print("tempInput.valueOneIsInput IS true")
//                if let selectedInputOneID = tempInput.selectedInputOne {
//                    newInput.selectedInputOne = fetchObjectByID(by: selectedInputOneID, entityType: Input.self)
//                } else {
//                    // Handle the case where tempInput.selectedInputOne is nil, if needed
//                }
//            } else {
//                newInput.valueOne = tempInput.valueOne ?? 88
//            }
//            print("Value One: \(newInput.valueOne)")
//
//            if tempInput.valueTwoIsInput == true {
//                print("tempInput.valueTwoIsInput IS true")
//                if let selectedInputTwoID = tempInput.selectedInputTwo {
//                    newInput.selectedInputTwo = fetchObjectByID(by: selectedInputTwoID, entityType: Input.self)
//                } else {
//                    // Handle the case where tempInput.selectedInputOne is nil, if needed
//                }
//            } else {
//                newInput.valueTwo = tempInput.valueTwo ?? 99
//            }
//            print("Value Two: \(newInput.valueTwo)")
//
//
//            newInput.previousInput = previousInput
//
//            if previousInput != nil {
//                previousInput?.nextInput = newInput
//            }
//
//            if tempInput.nextInput != nil {
//                previousInput = newInput
//            } else {
//                previousInput = nil
//            }
//
//        }
//
//        return newInput
//    }
//
//}
//

//extension DataService {
//
//    func inputAskForNumber(newInput: inout InputAskForNumber, tempInput: TempInput) {
//        newInput.id = tempInput.id
//        newInput.title = tempInput.title
//        let orderInt32: Int32 = Int32(tempInput.order)
//        newInput.order = orderInt32
//        newInput.inputType = tempInput.inputType.rawValue
//        newInput.userActionRequired = tempInput.userActionRequired
//
//        newInput.allowDecimals = tempInput.allowDecimals
//        newInput.allowNegatives = tempInput.allowNegatives
//        newInput.currency = tempInput.currency
//        newInput.promptBool = tempInput.promptBool
//        newInput.promptString = tempInput.promptString
//        newInput.useRange = tempInput.useRange
//        newInput.defaultValue = tempInput.defaultNumberValue
//        newInput.maxValue = tempInput.maxNumberValue
//        newInput.minValue = tempInput.minNumberValue
//        newInput.stepCount = tempInput.stepCount
//    }
//}
