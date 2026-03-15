//
//  InputFieldModel.swift
//  ActionStateExecution
//
//  Created by Zachary Sturman on 7/31/23.
//

import Foundation

struct InputFieldVariablesOld: Identifiable {
    let id = UUID()
    var name: String
    var prompt: String
    var selection: String
    
    // Text
    var textDefaultBool: Bool?
    var textDefault: String?
    
    // Count
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
    
    // Bool
    var boolDefault: Bool?
    
    // Number
    var numberDecimals: Bool?
    var numberNegative: Bool?
    var numberCurrency: Bool?
    var numberDefault: String?
    
    
    // Choose from List
    var listSelectMultiple: Bool?
    var listAddAtExecution: Bool?
    var listSelectedList: UUID?
    
    // Date
    
    // Location
    
    // Upload
    var uploadType: String?
    // type = [Image, Audio, Video]
    
    // Capture
    var captureType: String?
    // type = [Image, Audio, Video]
    
    // Other
    var otherType: String?
    // types = [Color, URL]

}
