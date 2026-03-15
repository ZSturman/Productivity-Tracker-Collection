//
//  BoolFieldVariables.swift
//  ActionStateExecution
//
//  Created by Zachary Sturman on 8/1/23.
//

import Foundation

class BoolFieldVariables {
    
    var selection: String?
    var boolDefault: Bool?
    
    init(selection: String? = nil,
         boolDefault: Bool? = nil)
    {
        self.selection = selection
        self.boolDefault = boolDefault
    }

}



