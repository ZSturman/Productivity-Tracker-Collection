//
//  InputModel.swift
//  Trackwell
//
//  Created by Zachary Sturman on 8/28/23.
//

import SwiftUI

class Input: Identifiable, ObservableObject {
    var id = UUID()
    var type: InputType
    var requiresInput: Bool
    var inputOutput: String
    var inputExecutions: [InputExecution] = []
    let order: String = UUID().uuidString
    
    // Properties that will be used to determine the inputOutput
    @Published var allowBlank: Bool = true
    @Published var provideDefault: Bool = false
    @Published var defaultValue: String = ""


    init(type: InputType) {
        self.type = type
        self.requiresInput = type.requiresInput
        self.inputOutput = type.inputOutput
    }
}

enum InputType: String, CaseIterable, Identifiable {
    case AskForText
    case SetText
    case AskForNumber
    case SetNumber
    case Calculate
    case GetLocation
    case Date

    var id: String {
        return self.rawValue
    }

    var requiresInput: Bool {
        switch self {
        case .AskForText, .AskForNumber:
            return true
        case .GetLocation, .Date, .SetText, .SetNumber, .Calculate:
            return false
        }
    }

    var inputOutput: String {
        switch self {
        case .AskForText:
            return "Hello World?"
        case .AskForNumber:
            return "######?"
        case .SetText:
            return "Hello World!"
        case .SetNumber:
            return "100"
        case .Calculate:
            return "100 + 100"
        case .GetLocation:
            return "Denver, CO"
        case .Date:
            return "06/01/1993"
        }
    }
}

