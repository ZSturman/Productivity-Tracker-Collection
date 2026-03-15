//
//  ExecutionModel.swift
//  Trackwell
//
//  Created by Zachary Sturman on 8/28/23.
//

import SwiftUI

class Execution: Identifiable {
    var id = UUID()
    var actionState: ActionState
    var trigger: Trigger
    var timestamp: Date = Date()
    var inputExecutions: [InputExecution] = []

    init(actionState: ActionState, trigger: Trigger) {
        self.actionState = actionState
        self.trigger = trigger
    }
}


class InputExecution: Identifiable {
    var id = UUID()
    var input: Input
    var title: String
    var order: Int

    init(input: Input, title: String, order: Int) {
        self.input = input
        self.title = title
        self.order = order
    }
}
