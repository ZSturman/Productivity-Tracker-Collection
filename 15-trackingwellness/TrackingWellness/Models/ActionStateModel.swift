//
//  ActionStateModel.swift
//  TrackingWellness
//
//  Created by Zachary Sturman on 8/30/23.
//

import Foundation
import SwiftUI

class ActionState: ObservableObject {
    var id = UUID()
    @Published var title: String
    
    init(title: String) {
        self.title = title
    }
}

class ActionStateVM: ObservableObject {
    @Published var actionState: ActionState
    
    init(actionState: ActionState) {
        self.actionState = actionState
    }
}
