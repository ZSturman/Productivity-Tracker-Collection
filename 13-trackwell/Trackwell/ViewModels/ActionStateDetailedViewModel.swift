//
//  ActionStateDetailedViewModel.swift
//  Trackwell
//
//  Created by Zachary Sturman on 8/26/23.
//


import SwiftUI

class ActionStateDetailedViewModel: ObservableObject {
    @ObservedObject var actionStateListVM: ActionStateListViewModel
    
    @Published var actionState: ActionState
    @Published var showEditView: Bool = false
    @Published var currentInputIndex: Int = 0
    @Published var currentTrigger: Trigger?
    //@Published var currentInput: Input?

    @Published var textInputValue: String = ""
    
    @Published var showTextInputSheet: Bool = false
    @Published var showDateInputSheet: Bool = false
    @Published var showLocationInputSheet: Bool = false
    @Published var showNumberInputSheet: Bool = false
    
    @Published var showAskForNumberInputSheet: Bool = false
    @Published var showAskForTextInputSheet: Bool = false
    @Published var showCalculateInputSheet: Bool = false
    
    @Published var showDateInputAlert: Bool = false
    
    @Published var showExecutionNotification: Bool = false
    @Published var executionNotificationContent: String = ""
    
    init(actionState: ActionState, actionStateListVM: ActionStateListViewModel) {
        self.actionState = actionState
        self.actionStateListVM = actionStateListVM
    }
    
    func startProcessingInputs(for trigger: Trigger) {
        if let firstInput = trigger.inputs.first {
            currentInputIndex = 0
            currentTrigger = trigger
            //currentInput = firstInput
            showSheet(for: firstInput.type)
        }
    }
    
    // Process the next input for the current trigger
    func processNextInput() {
        if let trigger = currentTrigger,
           currentInputIndex < trigger.inputs.count - 1 {
            currentInputIndex += 1
            showSheet(for: trigger.inputs[currentInputIndex].type)
        } else {
            endInputProcessing()
        }
    }
    
    // End the input processing and reset variables
    func endInputProcessing() {
        if let trigger = currentTrigger {
            let execution = Execution(actionState: self.actionState, trigger: trigger)
            for (index, input) in trigger.inputs.enumerated() {
                let inputExecution = InputExecution(input: input, title: input.type.rawValue, order: index)
                execution.inputExecutions.append(inputExecution)
            }
            self.actionState.executions.append(execution)
        }

        currentInputIndex = 0
        currentTrigger = nil
    }

    
    func showSheet(for inputType: InputType) {
        switch inputType {
        case .AskForNumber:
            showAskForNumberInputSheet = false
            showAskForNumberInputSheet = true
        case .AskForText:
            showAskForTextInputSheet = false
            showAskForTextInputSheet = true
        case .Calculate, .SetText, .Date, .GetLocation, .SetNumber:
            showExecutionNotification = false
            showExecutionNotification = true
        }
    
    }
    

    
    func deleteActionState(completion: @escaping () -> Void) {
        if let index = actionStateListVM.actionStates.firstIndex(where: { $0.id == actionState.id }) {
            actionStateListVM.actionStates.remove(at: index)
            print("Action State Deleted")
            completion()
        }
    }

}

