//
//  ActionStateRowViewModel.swift
//  Trackwell
//
//  Created by Zachary Sturman on 8/26/23.
//

import Foundation
import Combine

class ActionStateRowViewModel: ObservableObject {
    @Published var actionState: ActionState
    var actionStateListVM: ActionStateListViewModel

    init(actionState: ActionState, actionStateListVM: ActionStateListViewModel) {
        self.actionState = actionState
        self.actionStateListVM = actionStateListVM
    }
    


    var containsQuickActionButtonOne: Bool {
        return actionState.triggers.contains { $0.type == .QuickActionButtonOne }
    }
    func handleQuickActionButtonOnePressed() {
        print("Pressed Number One")
    }

    
    
    var containsQuickActionButtontwo: Bool {
        return actionState.triggers.contains { $0.type == .QuickActionButtonTwo }
    }
    func handleQuickActionButtontwoPressed() {
        print("Pressed Number Two")
    }
    
    
}


