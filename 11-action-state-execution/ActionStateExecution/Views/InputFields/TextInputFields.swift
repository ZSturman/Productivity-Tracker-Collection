//
//  TextInputFields.swift
//  ActionStateExecution
//
//  Created by Zachary Sturman on 8/1/23.
//

import SwiftUI

struct TextInputFields: View, FieldCreator {
    
    @Binding var selection: String
    
    @Binding var textDefaultBool: Bool
    @Binding var textDefault: String

   
    var body: some View {
        Section(header: Text("\(selection)"), footer: Text("Add a default value for quick execution")) {
            Toggle("Add default", isOn: $textDefaultBool)
            if textDefaultBool {
                TextField("Default text", text: $textDefault)
            }
        }

    }
    
    func createField(name: String, prompt: String) -> InputFieldVariables {
        InputFieldVariables(name: name,
              prompt: prompt,
              selection: selection,
              textDefaultBool: textDefaultBool,
              textDefault: textDefault)
    }
    
    func populateField(with field: InputFieldVariables) {
        self.selection = field.selection
        self.textDefaultBool = field.textDefaultBool ?? false
        self.textDefault = field.textDefault ?? ""

    }
}
