//
//  CountFieldVariables.swift
//  ActionStateExecution
//
//  Created by Zachary Sturman on 8/1/23.
//

import Foundation

class CountFieldVariables {
    
    var selection: String?
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
    
    init(selection: String? = nil,
         countDirection: String? = nil,
         countDecimals: Bool? = nil,
         countNegatives: Bool? = nil,
         countCurrency: Bool? = nil,
         countTo: Bool? = nil,
         countToValue: String? = nil,
         countToResult: String? = nil,
         countToAlertBool: Bool? = nil,
         countFrom: Bool? = nil,
         countFromValue: String? = nil,
         stepCountValue: String? = nil)
    {
        self.selection = selection
        self.countDirection = countDirection
        self.countDecimals = countDecimals
        self.countNegatives = countNegatives
        self.countCurrency = countCurrency
        self.countTo = countTo
        self.countToValue = countToValue
        self.countToResult = countToResult
        self.countToAlertBool = countToAlertBool
        self.countFrom = countFrom
        self.countFromValue = countFromValue
        self.stepCountValue = stepCountValue
    }

}



