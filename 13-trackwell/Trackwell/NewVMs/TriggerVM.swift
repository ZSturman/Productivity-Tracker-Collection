////
////  TriggerVM.swift
////  Trackwell
////
////  Created by Zachary Sturman on 8/30/23.
////
//
//import Foundation
//import SwiftUI
//
//class TriggerVM: ObservableObject {
//    @Published var trigger: Trigger
//    @Published var inputs: [InputVM] = []
//    
//    init(existingTrigger: Trigger? = nil, triggerType: TriggerType = .QuickActionButtonOne) {
//        if let providedTrigger = existingTrigger {
//            self.trigger = providedTrigger
//        } else {
//            // Assuming the Trigger class has a constructor that accepts type: TriggerType
//            self.trigger = Trigger(type: triggerType)
//        }
//    }
//    
//    func addInput(inputType: InputType) {
//        let inputVM = InputVM(inputType: inputType)
//        inputs.append(inputVM)
//    }
//    
//    
//}
