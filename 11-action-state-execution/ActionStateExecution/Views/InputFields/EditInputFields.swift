//
//  InputFields.swift
//  ActionStateExecution
//
//  Created by Zachary Sturman on 7/30/23.
//

import SwiftUI

struct EditInputFields: View {
    @Environment(\.presentationMode) var presentationMode

    @State private var selection = "Text"
    
    @State var variableName: String = ""
    @State var prompt: String = ""
    
    @State private var textDefaultBool = false
    @State private var textDefault: String = ""
    
    @State private var countDirection: String = "Ascending"
    @State private var countDecimals = false
    @State private var countNegatives = false
    @State private var countCurrency = false
    @State private var countTo = false
    @State private var countToValue: String = "100"
    @State private var countToResult: String = "Start over"
    @State private var countToAlertBool = false
    @State private var countFrom = true
    @State private var countFromValue: String = "0"
    @State private var stepCountValue: String = "1"
    
    @State private var boolDefault = true
    
    @State private var numberDecimals = false
    @State private var numberNegative = false
    @State private var numberCurrency = false
    @State private var numberDefault: String = "0"
    
    @State private var listSelectMultiple = false
    @State private var listAddAtExecution = false
    @State private var listSelectedList: UUID? = UUID()
    
    @State private var uploadType: String = ""
    
    @State private var captureType: String = ""
    
    @State private var otherType: String = ""
    
    @Binding var field: InputFieldVariables
    var onFinish: ((InputFieldVariables) -> Void)? = nil
    
    var body: some View {
        NavigationView {
            Form {
                Section(header: Text("Variable Details")) {
                    TextField("Name", text: $variableName)
                    TextField("Prompt", text: $prompt)
                    
               
                     Picker("Input type", selection: $selection) {
                         Text("Text").tag("Text")
                         Text("Count").tag("Count")
                         Text("Bool").tag("Bool")
                         Text("Number").tag("Number")
                         Text("Choose from list").tag("Choose from list")
                         Text("Date/Time").tag("Date/Time")
                         Text("Location").tag("Location")
                         Text("Upload").tag("Upload")
                         Text("Capture").tag("Capture")
                         Text("Other").tag("Other")
                     }
                }

                
                switch selection {
                case "Text":
                    TextInputFields(selection: $selection, textDefaultBool: $textDefaultBool, textDefault: $textDefault)
                case "Count":
                    CountInputFields(selection: $selection, countDirection: $countDirection, countDecimals: $countDecimals, countNegatives: $countNegatives, countCurrency: $countCurrency, countTo: $countTo, countToValue: $countToValue, countToResult: $countToResult, countToAlertBool: $countToAlertBool, countFrom: $countFrom, countFromValue: $countFromValue, stepCountValue: $stepCountValue)
                case "Bool":
                    BoolInputFields(selection: $selection, boolDefault: $boolDefault)
                case "Number":
                    NumberInputFields(selection: $selection, numberDecimals: $numberDecimals, numberNegative: $numberNegative, numberCurrency: $numberCurrency, numberDefault: $numberDefault)
                case "Choose from list":
                    ListInputFields(selection: $selection, listSelectMultiple:$listSelectMultiple, listAddAtExecution:$listAddAtExecution, listSelectedList: $listSelectedList)
                case "Date/Time":
                   Text("Date/Time")
                case "Location":
                   Text("Location")
                case "Upload":
                    Text("Upload")
                case "Capture":
                    Text("Capture")
                case "Other":
                  Text("Other")
                default:
                    Text("You're viewing the Text view")
                        .font(.caption)
                }
            }
            .navigationTitle("Manual Input")
            .navigationBarTitleDisplayMode(.inline)
            .navigationBarItems(
                leading: Button("Cancel") {
                    presentationMode.wrappedValue.dismiss()
                },
                trailing: Button("Done") {
                    field.name = variableName
                    field.prompt = prompt
                    field.selection = selection
                    field.textDefaultBool = textDefaultBool
                    field.textDefault = textDefault
                    field.countDirection = countDirection
                    field.countDecimals = countDecimals
                    field.countNegatives = countNegatives
                    field.countCurrency = countCurrency
                    field.countTo = countTo
                    field.countToValue = countToValue
                    field.countToResult = countToResult
                    field.countToAlertBool = countToAlertBool
                    field.countFrom = countFrom
                    field.countFromValue = countFromValue
                    field.stepCountValue = stepCountValue
                    field.boolDefault = boolDefault
                    field.numberDecimals = numberDecimals
                    field.numberNegative = numberNegative
                    field.numberCurrency = numberCurrency
                    field.numberDefault = numberDefault
                    field.listSelectMultiple = listSelectMultiple
                    field.listAddAtExecution = listAddAtExecution
                    field.listSelectedList = listSelectedList
                    field.uploadType = uploadType
                    field.captureType = captureType
                    field.otherType = otherType
                    
                    onFinish?(field)
                    presentationMode.wrappedValue.dismiss()
                }
            )
            .onAppear {
                self.variableName = field.name
                self.prompt = field.prompt
                self.selection = field.selection
                self.textDefaultBool = field.textDefaultBool ?? false
                self.textDefault = field.textDefault ?? ""
                self.countDirection = field.countDirection ?? ""
                self.countDecimals = field.countDecimals ?? false
                self.countNegatives = field.countNegatives ?? false
                self.countCurrency = field.countCurrency ?? false
                self.countTo = field.countTo ?? false
                self.countToValue = field.countToValue ?? ""
                self.countToResult = field.countToResult ?? ""
                self.countToAlertBool = field.countToAlertBool ?? false
                self.countFrom = field.countFrom ?? true
                self.countFromValue = field.countFromValue ?? "0"
                self.stepCountValue = field.stepCountValue ?? "1"
                self.boolDefault = field.boolDefault ?? true
                self.numberDecimals = field.numberDecimals ?? false
                self.numberNegative = field.numberNegative ?? false
                self.numberCurrency = field.numberCurrency ?? false
                self.numberDefault = field.numberDefault ?? "0"
                self.listSelectMultiple = field.listSelectMultiple ?? false
                self.listAddAtExecution = field.listAddAtExecution ?? false
                self.listSelectedList = field.listSelectedList
                self.uploadType = field.uploadType ?? ""
                self.captureType = field.captureType ?? ""
                self.otherType = field.otherType ?? ""
            }
        }
    }
}
