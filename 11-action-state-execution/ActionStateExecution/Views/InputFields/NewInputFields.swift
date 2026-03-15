//
//  InputFields.swift
//  ActionStateExecution
//
//  Created by Zachary Sturman on 7/30/23.
//

import SwiftUI

struct NewInputFields: View {
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
    
    var field: InputFieldVariables? = nil
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
                    let newField = InputFieldVariables(
                        name: variableName,
                        prompt: prompt,
                        selection: selection,
                        
                        textDefaultBool: textDefaultBool,
                        textDefault: textDefault,
                        
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
                        stepCountValue: stepCountValue,

                        boolDefault: boolDefault,
                        
                        numberDecimals: numberDecimals,
                        numberNegative: numberNegative,
                        numberCurrency: numberCurrency,
                        numberDefault: numberDefault,
                        
                        listSelectMultiple: listSelectMultiple,
                        listAddAtExecution: listAddAtExecution,
                        listSelectedList: listSelectedList,

                        uploadType: uploadType,
                        captureType: captureType,
                        otherType: otherType
                    )
                    onFinish?(newField)
                    presentationMode.wrappedValue.dismiss()
                }
            )
            .onAppear {
                if let existingField = field {
                    self.variableName = existingField.name
                    self.prompt = existingField.prompt
                    self.selection = existingField.selection

                    self.textDefaultBool = existingField.textDefaultBool ?? false
                    self.textDefault = existingField.textDefault ?? ""

                    self.countDirection = existingField.countDirection ?? ""
                    self.countDecimals = existingField.countDecimals ?? false
                    self.countNegatives = existingField.countNegatives ?? false
                    self.countCurrency = existingField.countCurrency ?? false
                    self.countTo = existingField.countTo ?? false
                    self.countToValue = existingField.countToValue ?? ""
                    self.countToResult = existingField.countToResult ?? ""
                    self.countToAlertBool = existingField.countToAlertBool ?? false
                    self.countFrom = existingField.countFrom ?? true
                    self.countFromValue = existingField.countFromValue ?? "0"
                    self.stepCountValue = existingField.stepCountValue ?? "1"

                    self.boolDefault = existingField.boolDefault ?? true

                    self.numberDecimals = existingField.numberDecimals ?? false
                    self.numberNegative = existingField.numberNegative ?? false
                    self.numberCurrency = existingField.numberCurrency ?? false
                    self.numberDefault = existingField.numberDefault ?? ""
                    
                    self.listSelectMultiple = existingField.listSelectMultiple ?? false
                    self.listAddAtExecution = existingField.listAddAtExecution ?? false
                    self.listSelectedList = existingField.listSelectedList ?? UUID()

                    self.uploadType = existingField.uploadType ?? ""
                    self.captureType = existingField.captureType ?? ""
                    self.otherType = existingField.otherType ?? ""
                }
            }


        }

    }
}


struct InputFields_Previews: PreviewProvider {
    static var previews: some View {
        NewInputFields()
    }
}


