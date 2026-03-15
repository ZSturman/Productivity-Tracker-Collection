////
////  ExecutionVM.swift
////  Trackwell
////
////  Created by Zachary Sturman on 8/30/23.
////
//
//import Foundation
//import SwiftUI
//
//class ExecutionVM: ObservableObject {
//    @Published var execution: Execution
//    @Published var inputExecutions: [InputExecutionVM] = []
//    
//    init(execution: Execution? = nil, triggerID: Trigger.ID) {
//        if let existingExecution = execution {
//            self.execution = existingExecution
//        } else {
//            self.execution = Execution(triggerID: triggerID)
//        }
//    }
//    
//    func addInputExecution(inputID: Input.ID, inputOutput: String) {
//        let inputExecutionVM = InputExecutionVM(inputID: inputID, inputOutput: inputOutput)
//        inputExecutions.append(inputExecutionVM)
//    }
//    
//}
