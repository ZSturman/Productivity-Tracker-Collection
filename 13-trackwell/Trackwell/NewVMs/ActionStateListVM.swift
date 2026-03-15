////
////  ActionStateListVM.swift
////  Trackwell
////
////  Created by Zachary Sturman on 8/30/23.
////
//import Foundation
//import SwiftUI
//
//class ActionStateListVM: ObservableObject {
//    @Published var actionStates: [ActionStateVM] = []
//    
//    func addActionState(actionStateVM: ActionStateVM) {
//        if let existingIndex = actionStates.firstIndex(where: { $0.actionState.id == actionStateVM.actionState.id }) {
//            actionStates[existingIndex] = actionStateVM
//        } else {
//            actionStates.append(actionStateVM)
//        }
//    }
//}
