//
//  AddManualInputFormView.swift
//  ActionStates
//
//  Created by Zachary Sturman on 7/23/23.
//
import SwiftUI



struct SelectManualInputInputTypeView: View {
    @Environment(\.managedObjectContext) var moc
    @Environment(\.presentationMode) var presentationMode
    @Binding var inputType: String

    
    let inputTypes = ["Number", "Range", "Text", "Boolean", "Date", "Time"]
    
    var body: some View {
        List {
            Section(footer: Text("This represents the data type to collect.")) {
                Picker(selection: $inputType, label: EmptyView()) {
                    ForEach(inputTypes, id: \.self) {
                        Text($0).tag($0)
                    }
                }
                .pickerStyle(.inline)
                .onChange(of: inputType) { newValue in
                    // Dismiss the view when a selection is made
                    self.presentationMode.wrappedValue.dismiss()
                }
            }
        }
    }
}


struct AddManualInputFormView: View {
    @Environment(\.managedObjectContext) var moc
    @Environment(\.dismiss) var dismiss
    @Environment(\.presentationMode) var presentationMode

    
    @State private var inputType = "Input Type"
    @State private var prompt = ""
    @State private var addPrompt = true
    
    @State private var negativeNumbers = false
    @State private var decimalNumbers = false
    @State private var rangeStart = 0
    @State private var rangeEnd = 10

    @State private var addDefaultValue = false
    @State private var defaultValueNumber: Double = 0

    @State private var booleanState = false
    @State private var defaultBooleanState = false

    @State private var defaultDate = Date()
    @State private var defaultTime = Date()
    
    @State private var isInputTypeSheetPresented = false
    @State private var inputTypeDetails = InputTypeDetails(inputType: "Input Type")


        
    var body: some View {
        
        VStack {
            Section {
                HStack(spacing: 20) {
                     Button(action: {
                         // This line will dismiss the sheet
                         presentationMode.wrappedValue.dismiss()
                     }) {
                         Text("Cancel")
                     }
                     Spacer() // Creates space between the two buttons
                     Button(action: {
                        let manualInput = ManualInputEntity(context: moc)
                         manualInput.id = UUID()
                        manualInput.numberValue = defaultValueNumber
                        manualInput.inputType = inputType
                         if addPrompt {
                            manualInput.prompt = prompt
                         } else {
                             manualInput.prompt = nil
                         }
                         manualInput.booleanValue = booleanState
                         manualInput.dateValue = defaultDate
                         manualInput.timeValue = defaultTime
     

                         presentationMode.wrappedValue.dismiss()
                     }) {
                         Text("Save")
                     }
                     .disabled(inputType == "Input Type") // The button will be disabled if inputType is "Input Type"
                 }
                .padding()
             }
            Form {
                     Section {
                         Toggle(isOn: $addPrompt) {
                             Text("Add prompt")
                         }

                         if addPrompt {
                             TextField(inputTypeDetails.prompt, text: $prompt)
                         }
                     }

                Button(action: { self.isInputTypeSheetPresented.toggle() }) {
                    Text(inputType.isEmpty ? "Select input type" : inputType)
                }
                .sheet(isPresented: $isInputTypeSheetPresented) {
                    SelectManualInputInputTypeView(inputType: self.$inputType)
                    // Removed inputDetails since it's not declared
                }
                .onChange(of: inputType) { newValue in
                    inputTypeDetails.inputType = newValue
                }


                    
                    if inputType == "Number" {
                        Toggle(isOn: $negativeNumbers) {
                            Text("Negative Numbers")
                        }
                        Toggle(isOn: $decimalNumbers) {
                            Text("Decimals")
                        }
                        
                        Toggle(isOn: $addDefaultValue) {
                            Text("Add Default Value")
                        }
                        
                        if addDefaultValue {
                            DefaultValueNumberView(defaultValueNumber: $defaultValueNumber)
                        }
                        
                        
                        
                    } else if inputType == "Range" {
                        Stepper(value: $rangeStart, in: 0...100, step: 1) {
                            Text("Start: \(rangeStart)")
                        }.onChange(of: rangeStart) { newValue in
                            if defaultValueNumber < Double(newValue) {
                                defaultValueNumber = Double(newValue)
                            }
                        }
                        Stepper(value: $rangeEnd, in: 0...100, step: 1) {
                            Text("End: \(rangeEnd)")
                        }.onChange(of: rangeEnd) { newValue in
                            if defaultValueNumber > Double(newValue) {
                                defaultValueNumber = Double(newValue)
                            }
                        }
                        
                        DefaultValueNumberView(defaultValueNumber: $defaultValueNumber)
                        
                        
                    } else if inputType == "Boolean" {
                        Toggle(isOn: $defaultBooleanState) {
                            Text("Default State")
                        }
                    }
                    
                }

             }
        }
     
     }
