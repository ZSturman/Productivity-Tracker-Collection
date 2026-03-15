//
//  TriggerModel.swift
//  Trackwell
//
//  Created by Zachary Sturman on 8/28/23.
//

import SwiftUI


class Trigger: Identifiable, ObservableObject {
    var id = UUID()
    var selectedIcon: String?
    var selectedColor: String?
    var type: TriggerType
    var executions: [Execution] = []
    var inputs: [Input] = []
    var triggerOutput: String = ""
    
    //var actionState: ActionState?

    init(type: TriggerType) {
        self.type = type
    }
    
    func updateTriggerOutput() {
        if let lastInput = inputs.last {
            triggerOutput = lastInput.inputOutput
        }
    }
}

enum TriggerType: String, CaseIterable, Identifiable {
    case QuickActionButtonOne = "Quick Action Btn 1"
    case QuickActionButtonTwo = "Quick Action Btn 2"
    case SwipeLeftOne = "Swipe Left One"

    var id: String {
        return self.rawValue
    }
}

