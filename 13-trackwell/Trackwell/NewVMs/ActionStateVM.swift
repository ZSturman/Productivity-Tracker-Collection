////
////  ActionStateVM.swift
////  Trackwell
////
////  Created by Zachary Sturman on 8/30/23.
////
//
//import Foundation
//import SwiftUI
//
//class ActionStateVM: ObservableObject, Identifiable {
//    var vmID = UUID()
//    @ObservedObject var actionStateListVM: ActionStateListVM
//    @Published var actionState: ActionState
//    
//    @Published var title: String = ""
//    @Published var isAction: Bool = true
//    
//    @Published var triggers: [TriggerVM] = []
//    @Published var executions: [ExecutionVM] = []
//    @Published var isNew: Bool
//    
//    init(actionStateListVM: ActionStateListVM, editingActionState: ActionState? = nil) {
//        self.actionStateListVM = actionStateListVM
//
//        if let editingActionState = editingActionState {
//            self.isNew = false
//            self.actionState = editingActionState
//            self.title = editingActionState.title
//            self.isAction = editingActionState.isAction
//        } else {
//            self.actionState = ActionState(title: "", isAction: true)
//            self.isNew = true
//        }
//
//    }
//    
//    func addTrigger(triggerType: TriggerType) {
//        let triggerVM = TriggerVM(triggerType: triggerType)
//        triggers.append(triggerVM)
//    }
//    
//    func addExecution(triggerID: Trigger.ID) {
//        let executionVM = ExecutionVM(triggerID: triggerID)
//        executions.append(executionVM)
//    }
//    
//    func saveActionState() {
//        actionState.title = title
//        actionState.isAction = isAction
//        actionStateListVM.actionStates.append(self)
//    }
//}
