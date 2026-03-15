//
//  BoolInputFields.swift
//  ActionStateExecution
//
//  Created by Zachary Sturman on 8/1/23.
//


import SwiftUI
struct BoolInputFields: View, FieldCreator {
    
    @Binding var selection: String
    @Binding var boolDefault: Bool

    @State var boolExplanation: String = ""

    // Helper function to return the capitalized string representation of a boolean
    func capitalizedString(for bool: Bool) -> String {
        return bool.description.capitalized
    }

    var body: some View {
        Section(header: Text("\(selection)"), footer: Text(boolExplanation)) {
            Toggle("Default value", isOn: $boolDefault)
                .onChange(of: boolDefault) { newValue in
                    boolExplanation = "Boolean value when initially executing: " + capitalizedString(for: newValue)
                }
        }
        .onAppear {
            boolExplanation = "Boolean value when initially executing: " + capitalizedString(for: boolDefault)
        }
    }

    func createField(name: String, prompt: String) -> InputFieldVariables {
        InputFieldVariables(name: name,
              prompt: prompt,
              selection: selection,
              boolDefault: boolDefault)
    }
    
    func populateField(with field: InputFieldVariables) {
        self.selection = field.selection
        self.boolDefault = field.boolDefault ?? false
    }
}
