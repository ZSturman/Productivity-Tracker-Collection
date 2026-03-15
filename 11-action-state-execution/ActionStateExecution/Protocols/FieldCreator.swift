//
//  FieldCreator.swift
//  ActionStateExecution
//
//  Created by Zachary Sturman on 7/31/23.
//

// FieldCreator.swift

import Foundation

protocol FieldCreator {
    func createField(name: String, prompt: String) -> InputFieldVariables
    func populateField(with field: InputFieldVariables)
}

