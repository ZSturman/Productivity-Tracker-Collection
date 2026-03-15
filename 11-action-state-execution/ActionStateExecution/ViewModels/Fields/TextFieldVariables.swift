//
//  TextFieldVariables.swift
//  ActionStateExecution
//
//  Created by Zachary Sturman on 8/1/23.
//

import SwiftUI

class TextFieldVariables: FieldVariables {
    var selection: String?
    var textDefaultBool: Bool?
    var textDefault: String?
    
    init(selection: String? = nil,
         textDefaultBool: Bool? = nil,
         textDefault: String? = nil)
    {
        self.selection = selection
        self.textDefaultBool = textDefaultBool
        self.textDefault = textDefault
    }

}



