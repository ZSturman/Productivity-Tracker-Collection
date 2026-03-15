//
//  NumberInputFields.swift
//  ActionStateExecution
//
//  Created by Zachary Sturman on 8/1/23.
//

import SwiftUI

struct NumberInputFields: View, FieldCreator {
    
    @Binding var selection: String
    
    @Binding var numberDecimals: Bool
    @Binding var numberNegative: Bool
    @Binding var numberCurrency: Bool
    @Binding var numberDefault: String

   
    var body: some View {
        Section(header: Text("\(selection)"), footer: Text("Types of numbers allowed")) {
            Toggle("Decimals", isOn: $numberDecimals)
            Toggle("Negatives", isOn: $numberNegative)
            Toggle("Currency", isOn: $numberCurrency)
        }
        
        Section {
            TextField("Default", text: $numberDefault)
        }

    }
    
    func createField(name: String, prompt: String) -> InputFieldVariables {
        InputFieldVariables(name: name,
              prompt: prompt,
              selection: selection,
              numberDecimals: numberDecimals,
              numberNegative: numberNegative,
              numberCurrency: numberCurrency,
              numberDefault: numberDefault)
    }
    
    func populateField(with field: InputFieldVariables) {
        self.selection = field.selection
        self.numberDecimals = field.numberDecimals ?? false
        self.numberNegative = field.numberNegative ?? false
        self.numberCurrency = field.numberCurrency ?? false
        self.numberDefault = field.numberDefault ?? "0"

    }
}
