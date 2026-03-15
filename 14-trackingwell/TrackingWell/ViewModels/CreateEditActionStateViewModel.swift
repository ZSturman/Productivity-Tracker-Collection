//
//  CreateEditActionStateViewModel.swift
//  TrackingWell
//
//  Created by Zachary Sturman on 8/30/23.
//
import Foundation
import CoreData
import SwiftUI

class CreateEditActionStateViewModel: ObservableObject {
    @Published var actionState: ActionState
    @Published var isAction: Bool
    @Published var title: String
    @Published var triggers: [Trigger] = []
    @Published var inputs: [Input] = []
    
    private let dataController = DataController.shared
    @Published var isEditMode: Bool

    init(actionState: ActionState? = nil) {
        if let existingActionState = actionState {
            print("Initializing ViewModel in edit mode with existing ActionState: \(existingActionState)")
            self.actionState = existingActionState
            self.isAction = existingActionState.isAction
            self.title = existingActionState.title ?? ""
            self.isEditMode = true
            loadTriggers()
        } else {
            print("Initializing ViewModel in creation mode")
            self.actionState = dataController.createActionState(in: dataController.newContext)
            self.isAction = false  // Default value
            self.title = ""  // Default value
            self.isEditMode = false
        }
    }


    private func loadTriggers() {
        print("Loading triggers for ActionState: \(actionState)")
        self.triggers = actionState.triggers?.allObjects as? [Trigger] ?? []
    }
    
    func loadInputs(for trigger: Trigger) {
        print("Loading inputs for Trigger: \(trigger)")
        if let triggerInputs = trigger.inputs?.allObjects as? [Input] {
            self.inputs.append(contentsOf: triggerInputs)
        }
    }

    func addTrigger(trigger: Trigger) {
        print("Adding new Trigger: \(trigger)")
        triggers.append(trigger)
    }

    func deleteTrigger(at offsets: IndexSet) {
        print("Deleting Trigger at offsets: \(offsets)")
        for index in offsets {
            let triggerToDelete = triggers[index]
            do {
                try dataController.delete(triggerToDelete, in: dataController.newContext)
            } catch {
                print("Error deleting trigger: \(error)")
            }
        }
        triggers.remove(atOffsets: offsets)
    }

    func addInput(input: Input) {
        print("Adding new Input: \(input)")
        inputs.append(input)
    }

    func deleteInput(at offsets: IndexSet) {
        print("Deleting Input at offsets: \(offsets)")
        for index in offsets {
            let inputToDelete = inputs[index]
            do {
                try dataController.delete(inputToDelete, in: dataController.newContext)
            } catch {
                print("Error deleting input: \(error)")
            }
        }
        inputs.remove(atOffsets: offsets)
    }


    func createNewTrigger(title: String) {
        let newTrigger = Trigger(context: dataController.newContext)
        newTrigger.id = UUID()
        newTrigger.title = title
        newTrigger.actionState = actionState
        triggers.append(newTrigger)
        
        do {
            try dataController.newContext.save()
        } catch {
            print("Error saving after creating Trigger: \(error)")
        }
    }


    func createNewInput(title: String, order: Int32, for trigger: Trigger) {
        print("Creating new Input with title: \(title) for Trigger: \(trigger)")
        let newInput = Input(context: dataController.newContext)
        newInput.id = UUID()
        newInput.title = title
        newInput.order = order
        newInput.trigger = trigger
        inputs.append(newInput)
    }

    func saveToCoreData() {
        print("Preparing to save to CoreData")
        // Sort inputs based on order before saving
        let sortedInputs = inputs.sorted(by: { $0.order < $1.order })
        inputs = sortedInputs
        
        actionState.isAction = isAction
        actionState.title = title

        do {
            if isEditMode {
                print("SAVING: In edit mode \(actionState.title ?? "No title")")
                try dataController.saveChanges(in: dataController.newContext)
            } else {
                print("SAVING: New ActionState \(actionState.title ?? "No title")")
                try dataController.saveChanges(in: dataController.newContext)
            }
        } catch {
            print("Error saving to CoreData: \(error)")
        }
    }


}

