//
//  ListFieldVariables.swift
//  ActionStateExecution
//
//  Created by Zachary Sturman on 8/1/23.
//

import Foundation

class ListFieldVariables {
    
    var selection: String?
    var listSelectMultiple: Bool?
    var listAddAtExecution: Bool?
    var listSelectedList: UUID?
    
    init(selection: String? = nil,
         listSelectMultiple: Bool? = nil,
         numberNegative: Bool? = nil,
         listAddAtExecution: Bool? = nil,
         listSelectedList: UUID? = nil)
    {
        self.selection = selection
        self.listSelectMultiple = listSelectMultiple
        self.listAddAtExecution = listAddAtExecution
        self.listSelectedList = listSelectedList
    }
}
