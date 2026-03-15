//
//  Validations.swift
//  BeingAnalytics
//
//  Created by Zachary Sturman on 9/22/23.
//


import Foundation

struct ValidationHelper {
    
    // Function to validate if minNumberValue is not greater than maxNumberValue
    static func validateMinMaxValues(minValue: Double, maxValue: Double, useRange: Bool) -> (isValid: Bool, errorMessage: String?) {
        if useRange && minValue > maxValue {
            return (false, "Minimum value cannot be greater than the maximum value.")
        }
        return (true, nil)
    }
    
    
    static func ensureNonNegativeValue(value: Double, allowNegatives: Bool) -> Double {
         let adjustedValue = !allowNegatives ? max(value, 0) : value
         print("ensureNonNegativeValue - Input Value: \(value), Adjusted Value: \(adjustedValue), allowNegatives: \(allowNegatives)")
         return adjustedValue
    }

    
    // Function to format number based on allowDecimals
    static func formatNumber(_ value: Double, allowDecimals: Bool) -> String {
        return allowDecimals ? String(format: "%.2f", value) : "\(Int(value))"
    }
    
    // Add other validation functions as needed
}
