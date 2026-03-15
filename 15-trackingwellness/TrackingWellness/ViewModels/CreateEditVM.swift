//
//  CreateEditVM.swift
//  TrackingWellness
//
//  Created by Zachary Sturman on 8/30/23.
//

import Foundation
import SwiftUI


class CreateEditVM: ObservableObject {
    @Published var actionState: ActionState
    @Published var actionStateVM: ActionStateVM
    
    init(editActionState: ActionState? = nil, actionStateVM: ActionStateVM) {
        if let actionState = editActionState {
            self.actionState = actionState
            self.actionStateVM = ActionStateVM(actionState: actionState)
        } else {
            let newActionState = ActionState(title: "")
            self.actionState = newActionState
            self.actionStateVM = ActionStateVM(actionState: newActionState)
        }
    }
}

  
