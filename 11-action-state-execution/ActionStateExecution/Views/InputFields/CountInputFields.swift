//
//  CountInputField.swift
//  ActionStateExecution
//
//  Created by Zachary Sturman on 7/31/23.
//

import SwiftUI

struct CountInputFields: View, FieldCreator {
    
    @Binding var selection: String
    
    @Binding var countDirection: String
    @Binding var countDecimals: Bool
    @Binding var countNegatives: Bool
    @Binding var countCurrency: Bool
    @Binding var countTo: Bool
    @Binding var countToValue: String
    @Binding var countToResult: String
    @Binding var countToAlertBool: Bool
    @Binding var countFrom: Bool
    @Binding var countFromValue: String
    @Binding var stepCountValue: String
    
    @State var countDirectionExplanation: String = "This is the definition of ascending"
    
    var body: some View {
        Section(header: Text("\(selection)"), footer: Text(countDirectionExplanation)) {
            Picker("Count direction", selection: $countDirection) {
                Text("Ascending").tag("Ascending")
                Text("Descending").tag("Descending")
                Text("Variable").tag("Variable")
            }
            .pickerStyle(.segmented)
            .onChange(of: countDirection) { newValue in
                switch newValue {
                case "Ascending":
                    countDirectionExplanation = "This is the definition of ascending"
                case "Descending":
                    countDirectionExplanation = "This is the definition of descending"
                case "Variable":
                    countDirectionExplanation = "This is the definition of variable"
                default:
                    countDirectionExplanation = ""
                }
            }
        }

        Section {
            Toggle("Decimals", isOn: $countDecimals)
            Toggle("Negatives", isOn: $countNegatives)
            Toggle("Currency", isOn: $countCurrency)
        }

        Section {
            Toggle("To", isOn: $countTo)
            if countTo {
                HStack {
                    Text("End at:")
                    Spacer()
                    TextField("", text: $countToValue)
                        .multilineTextAlignment(.trailing)
                }
                Picker("If count = \(countToValue)", selection: $countToResult){
                    Text("Start over").tag("Start over")
                    Text("Keep going").tag("Keep going")
                    Text("Stop counting").tag("Stop counting")
                }
                Toggle("Alert", isOn: $countToAlertBool)
            }
        }

        Section {
            Toggle("From", isOn: $countFrom)
            if countFrom {
                HStack {
                    Text("Start from:")
                    Spacer()
                    TextField("", text: $countFromValue)
                        .multilineTextAlignment(.trailing)
                }
            }
        }

        Section {
            HStack {
                Text("Step count")
                    .foregroundColor(countDirection == "Variable" ? .gray : .primary)
                Spacer()
                TextField("", text: $stepCountValue)
                    .disabled(countDirection == "Variable")
                    .foregroundColor(countDirection == "Variable" ? .gray : .primary)
                    .multilineTextAlignment(.trailing)
            }
        }
    }
    
    func createField(name: String, prompt: String) -> InputFieldVariables {
        InputFieldVariables(name: name,
              prompt: prompt,
              selection: selection,
              countDirection: countDirection,
              countDecimals: countDecimals,
              countNegatives: countNegatives,
              countCurrency: countCurrency,
              countTo: countTo,
              countToValue: countToValue,
              countToResult: countToResult,
              countToAlertBool: countToAlertBool,
              countFrom: countFrom,
              countFromValue: countFromValue,
              stepCountValue: stepCountValue)
    }
    
    func populateField(with field: InputFieldVariables) {
        self.selection = field.selection
        self.countDirection = field.countDirection ?? "Ascending"
        self.countDecimals = field.countDecimals ?? false
        self.countNegatives = field.countNegatives ?? false
        self.countCurrency = field.countCurrency ?? false
        self.countTo = field.countTo ?? false
        self.countToValue = field.countToValue ?? "100"
        self.countToResult = field.countToResult ?? "Start over"
        self.countToAlertBool = field.countToAlertBool ?? false
        self.countFrom = field.countFrom ?? true
        self.countFromValue = field.countFromValue ?? "0"
        self.stepCountValue = field.stepCountValue ?? "1"
    }
}
