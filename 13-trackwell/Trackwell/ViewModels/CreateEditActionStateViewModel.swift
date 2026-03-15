//
//  CreateEditActionStateViewModel.swift
//  Trackwell
//
//  Created by Zachary Sturman on 8/26/23.
//

import SwiftUI

class CreateEditActionStateViewModel: ObservableObject {
    @ObservedObject var actionStateListVM: ActionStateListViewModel
    
    @Published var actionState: ActionState
    @Published var actionStates: [ActionState]
    
    @Published var title: String = ""
    @Published var isAction: Bool = true
    @Published var selectedTriggers: [TriggerType] = []
    @Published var showTriggerOptions = false
    @Published var currentTriggerBeingEdited: TriggerType?
    @Published var inputsForTriggers: [Trigger: [Input]] = [:]
    @Published var lastInputOutputs: [Trigger: String] = [:]

    @Published var showInputOptions = false
    @Published var isNew: Bool

    init(actionStateListVM: ActionStateListViewModel, editingActionState: ActionState? = nil) {
        self.actionStateListVM = actionStateListVM
        self.actionStates = actionStateListVM.actionStates // Set from the shared ViewModel

        if let editingActionState = editingActionState {
            self.isNew = false
            self.actionState = editingActionState
            self.title = editingActionState.title
            self.isAction = editingActionState.isAction
            self.selectedTriggers = editingActionState.triggers.map { $0.type }
            self.inputsForTriggers = [:]
            for trigger in editingActionState.triggers {
                self.inputsForTriggers[trigger.id] = trigger.inputs
            }
        } else {
            self.actionState = ActionState(title: "", isAction: true)
            self.isNew = true
        }

    }


    func saveActionState() {
        actionState.title = title
        actionState.isAction = isAction
        actionState.triggers = selectedTriggers.map { triggerOption in
            let trigger = Trigger(type: triggerOption)
            trigger.inputs = inputsForTriggers[trigger.id] ?? []
            return trigger
        }
        
        // If the actionState is already present in the shared ViewModel, update it.
        // Otherwise, append it to the shared ViewModel's list.
        if let index = actionStateListVM.actionStates.firstIndex(where: { $0.id == actionState.id }) {
            actionStateListVM.actionStates[index] = actionState
        } else {
            actionStateListVM.actionStates.append(actionState)
        }
    }

    func updateLastInputOutput(for trigger: Trigger) {
        if let lastInput = inputsForTriggers[trigger.id]?.last {
            lastInputOutputs[trigger.id] = lastInput.inputOutput
        }
    }


    
    func deleteTrigger(_ trigger: Trigger) {
        if let index = selectedTriggers.firstIndex(of: trigger.type) {
            selectedTriggers.remove(at: index)
            inputsForTriggers[trigger.id] = nil
        }
    }

    func deleteInput(forTrigger trigger: Trigger, at offsets: IndexSet) {
        inputsForTriggers[trigger.id]?.remove(atOffsets: offsets)
    }

    func moveInput(forTrigger trigger: Trigger, from source: IndexSet, to destination: Int) {
        inputsForTriggers[trigger.id]?.move(fromOffsets: source, toOffset: destination)
    }
    
    func binding(for trigger: Trigger) -> Binding<[Input]> {
        return .init(
            get: { self.inputsForTriggers[trigger.id] ?? [] },
            set: { self.inputsForTriggers[trigger.id] = $0 }
        )
    }

}
