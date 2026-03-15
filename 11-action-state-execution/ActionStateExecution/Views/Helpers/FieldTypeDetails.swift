//
//  FieldTypeDetails.swift
//  ActionStateExecution
//
//  Created by Zachary Sturman on 7/28/23.
//

import Foundation
import Combine

class FieldTypeDetails: ObservableObject {
    @Published var fieldType: String

    var prompt: String {
        switch fieldType {
        case "Number":
            return "Enter a number..."
        case "Range":
            return "Enter a number within the range..."
        case "Text":
            return "Enter some text..."
        case "Boolean":
            return "Select true or false..."
        case "Date":
            return "Select a date..."
        case "Time":
            return "Select a time..."
        default:
            return "Enter value..."
        }
    }
    
    var explanation: String {
        switch fieldType {
        case "Number":
            return "The 'Number' type allows you to input numerical data."
        case "Range":
            return "The 'Range' type allows you to input a number within a specific range."
        case "Text":
            return "The 'Text' type allows you to input free-form text."
        case "Boolean":
            return "The 'Boolean' type allows you to choose between two binary options: True or False."
        case "Date":
            return "The 'Date' type allows you to select a specific date."
        case "Time":
            return "The 'Time' type allows you to select a specific time."
        default:
            return ""
        }
    }
    
    init(fieldType: String) {
        self.fieldType = fieldType
    }
}
