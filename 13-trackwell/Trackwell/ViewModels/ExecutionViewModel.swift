//
//  ExecutionViewModel.swift
//  Trackwell
//
//  Created by Zachary Sturman on 8/28/23.
//


import SwiftUI

class ExecutionViewModel: ObservableObject {
    @ObservedObject var actionStateListVM: ActionStateListViewModel
    
    @Published var actionState: ActionState
    
    init(actionState: ActionState, actionStateListVM: ActionStateListViewModel) {
        self.actionState = actionState
        self.actionStateListVM = actionStateListVM
    }
    
//    func startProcessingInputs(for trigger: Trigger) {
//        if let firstInput = trigger.inputs.first {
//            currentInputIndex = 0
//            currentTrigger = trigger
//            showSheet(for: firstInput.type)
//        }
//    }
//
//    func processNextInput() {
//        if let trigger = currentTrigger,
//           currentInputIndex < trigger.inputs.count - 1 {
//            currentInputIndex += 1
//            showSheet(for: trigger.inputs[currentInputIndex].type)
//        } else {
//            endInputProcessing()
//        }
//    }
//
//    func endInputProcessing() {
//        if let trigger = currentTrigger {
//            let execution = Execute(actionState: self.actionState, trigger: trigger)
//            for (index, input) in trigger.inputs.enumerated() {
//                let inputExecution = InputExecution(input: input, title: input.type.rawValue, order: index)
//                execution.inputExecutions.append(inputExecution)
//            }
//            self.actionState.executions.append(execution)
//        }
//
//        currentInputIndex = 0
//        currentTrigger = nil
//    }
//
//    func showSheet(for inputType: InputOptions) {
//        switch inputType {
//        case .AskForNumber:
//            showAskForNumberInputSheet = false
//            showAskForNumberInputSheet = true
//        case .AskForText:
//            showAskForTextInputSheet = false
//            showAskForTextInputSheet = true
//        case .Calculate, .SetText, .Date, .GetLocation, .SetNumber:
//            showExecutionNotification = false
//            executionNotificationContent = inputType.inputOutput
//            showExecutionNotification = true
//        }
//    }


    func handleQuickActionButtonOnePressed() {
        // Logic for handling quick action button press
        // This will be extracted from ActionStateRowView.swift or its ViewModel
    }
}
