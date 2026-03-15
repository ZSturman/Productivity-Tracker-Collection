//  NumberFieldVariables.swift
//  ActionStateExecution
//
//  Created by Zachary Sturman on 8/1/23.
//

import Foundation

class NumberFieldVariables: FieldVariables {
    
    var selection: String?
    var numberDecimals: Bool?
    var numberNegative: Bool?
    var numberCurrency: Bool?
    var numberDefault: String?
    
    init(selection: String? = nil,
         numberDecimals: Bool? = nil,
         numberNegative: Bool? = nil,
         numberCurrency: Bool? = nil,
         numberDefault: String? = nil)
    {
        self.selection = selection
        self.numberDecimals = numberDecimals
        self.numberNegative = numberNegative
        self.numberCurrency = numberCurrency
        self.numberDefault = numberDefault
    }
}
