//
//  InputTypes.swift
//  TrackingWell
//
//  Created by Zachary Sturman on 8/30/23.
//

import Foundation


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

