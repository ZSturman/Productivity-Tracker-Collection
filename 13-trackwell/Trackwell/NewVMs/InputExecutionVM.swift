////
////  InputExecutionVM.swift
////  Trackwell
////
////  Created by Zachary Sturman on 8/30/23.
////
//
//import Foundation
//import SwiftUI
//
//class InputExecutionVM: ObservableObject {
//    @Published var inputExecution: InputExecution
//    
//    init(inputExecution: InputExecution? = nil, inputID: Input.ID, inputOutput: String = "\(Date())") {
//        if let existingInputExecution = inputExecution {
//            self.inputExecution = existingInputExecution
//        } else {
//            self.inputExecution = InputExecution(inputID: inputID, inputOutput: inputOutput)
//        }
//    }
//    
//}
