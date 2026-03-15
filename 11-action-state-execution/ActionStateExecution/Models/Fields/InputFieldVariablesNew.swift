//
//  InputFieldVariablesNew.swift
//  ActionStateExecution
//
//  Created by Zachary Sturman on 8/4/23.
//

import SwiftUI

struct CommonFieldAttributes: Identifiable {
    let id = UUID()
    var name: String
    var prompt: String
    var selection: String
}

struct TextFieldAttributes: FieldVariables {
    var textDefaultBool: Bool?
    var textDefault: String?
}

struct CountFieldAttributes: FieldVariables {
    var countDirection: String?
    var countDecimals: Bool?
    var countNegatives: Bool?
    var countCurrency: Bool?
    var countTo: Bool?
    var countToValue: String?
    var countToResult: String?
    var countToAlertBool: Bool?
    var countFrom: Bool?
    var countFromValue: String?
    var stepCountValue: String?
}

struct BoolFieldAttributes: FieldVariables {
    var boolDefault: Bool?
}

struct NumberFieldAttributes: FieldVariables {
    var numberDecimals: Bool?
    var numberNegative: Bool?
    var numberCurrency: Bool?
    var numberDefault: String?
}

struct ListFieldAttributes: FieldVariables {
    var listSelectMultiple: Bool?
    var listAddAtExecution: Bool?
    var listSelectedList: UUID?
}

struct UploadFieldAttributes: FieldVariables {
    var uploadType: String? // type = [Image, Audio, Video]
}

struct CaptureFieldAttributes: FieldVariables {
    var captureType: String? // type = [Image, Audio, Video]
}

struct OtherFieldAttributes: FieldVariables {
    var otherType: String? // types = [Color, URL]
}


struct InputFieldVariables {
    var commonAttributes: CommonFieldAttributes
    var textFieldAttributes: TextFieldAttributes?
    var countFieldAttributes: CountFieldAttributes?
    var boolFieldAttributes: BoolFieldAttributes?
    var numberFieldAttributes: NumberFieldAttributes?
    var listFieldAttributes: ListFieldAttributes?
    var uploadFieldAttributes: UploadFieldAttributes?
    var captureFieldAttributes: CaptureFieldAttributes?
    var otherFieldAttributes: OtherFieldAttributes?
}

struct FieldVariable {
    var variable: String
    var value: String
}

protocol FieldVariables {
    func getVariables() -> [FieldVariable]
}

extension FieldVariables {
    func getVariables() -> [FieldVariable] {
        var fieldVariables: [FieldVariable] = []
        
        let mirror = Mirror(reflecting: self)
        for child in mirror.children {
            if let propertyName = child.label {
                var value = ""
                if let boolValue = child.value as? Bool {
                    value = boolValue ? "true" : "false"
                } else if let stringValue = child.value as? String {
                    value = stringValue
                } else if let uuidValue = child.value as? UUID {
                    value = uuidValue.uuidString
                } else if let dateValue = child.value as? Date {
                    // Use a date formatter to convert Date to String
                    let formatter = DateFormatter()
                    formatter.dateFormat = "yyyy-MM-dd HH:mm:ss"
                    value = formatter.string(from: dateValue)
                }
                
                let fieldVariable = FieldVariable(variable: propertyName, value: value)
                fieldVariables.append(fieldVariable)
            }
        }
        
        return fieldVariables
    }
}
