//
//  InputSheetView.swift
//  BeingAnalytics
// 
//  Created by Zachary Sturman on 9/1/23.
//

import SwiftUI

struct InputSheetView: View {
    @ObservedObject var actionStateExecutionVM: ActionStateExecutionVM
    @State private var localTextField: String = ""
    @State private var localNumberField: Double = 0.0
    @Environment(\.dismiss) private var dismiss
    
    init(actionStateExecutionVM: ActionStateExecutionVM) {
        self.actionStateExecutionVM = actionStateExecutionVM
        _localTextField = State(initialValue: actionStateExecutionVM.outputString)
        _localNumberField = State(initialValue: actionStateExecutionVM.outputNumber)
    }
    
    var body: some View {
        if actionStateExecutionVM.askForTextInput != nil {
            AskForTextInputSheetView(textInput: actionStateExecutionVM.askForTextInput!, textField: $localTextField)
        } else if actionStateExecutionVM.askForNumberInput != nil {
 
            if actionStateExecutionVM.askForNumberInput?.useRange == true {
                let numberRange = actionStateExecutionVM.askForNumberInput!.minValue...actionStateExecutionVM.askForNumberInput!.maxValue
                AskForNumberRangeInputSheetView(numberInput: actionStateExecutionVM.askForNumberInput!, numberField: $localNumberField, range: numberRange, step: actionStateExecutionVM.askForNumberInput!.stepCount)
            } else {
                AskForNumberInputSheetView(numberInput: actionStateExecutionVM.askForNumberInput!, numberField: $localNumberField)
            }

        } else {
            Text("No input type detected/ set")
        }
        
        HStack {
            Button(action: {
                actionStateExecutionVM.resetExecutionValues()
                dismiss()
            }, label: {
                Text("Cancel")
            })
            .buttonStyle(PlainButtonStyle())
            Spacer()
            Button("Done") {
                if actionStateExecutionVM.askForTextInput != nil {
                    actionStateExecutionVM.outputString = localTextField
                } else if actionStateExecutionVM.askForNumberInput != nil {
                    actionStateExecutionVM.outputNumber = localNumberField
                }
                actionStateExecutionVM.finalizeInput()
                dismiss()
            }
            .buttonStyle(PlainButtonStyle())
        }
        .padding()
    }
}

struct AskForTextInputSheetView: View {
    var textInput: InputAskForText
    
    @Binding var textField: String
    
    var body: some View {
        Form {
            Section(header: Text(textInput.title ?? "No Current Input")) {
                Text("\(textInput.order)")
                    .font(.caption)
            }
            
            if textInput.promptBool == true {
                Section {
                    Text(textInput.promptString ?? "Prompt here")
                }
            }
            TextField("Enter response...", text: $textField)
                .padding()
        }
    }
}



struct AskForNumberInputSheetView: View {
    var numberInput: InputAskForNumber
    
    @Binding var numberField: Double
    
    let decimalNumberFormatter: NumberFormatter = {
        let formatter = NumberFormatter()
        formatter.numberStyle = .decimal
        formatter.minimumFractionDigits = 2
        formatter.maximumFractionDigits = 2
        return formatter
    }()
    
    let numberFormatter: NumberFormatter = {
        let formatter = NumberFormatter()
        formatter.maximumFractionDigits = 0
        return formatter
    }()
    
    var body: some View {
        Form {
            Section(header: Text(numberInput.title ?? "No Current Input")) {
                Text("\(numberInput.order)")
                    .font(.caption)
            }
            
            if numberInput.promptBool == true {
                Section {
                    Text(numberInput.promptString ?? "Prompt here")
                }
            }
            
            if numberInput.allowDecimals == true {
                TextField("Enter response...", value: $numberField, formatter: decimalNumberFormatter)
                    .keyboardType(.decimalPad)
                    .padding()
            } else {
                TextField("Enter response...", value: $numberField, formatter: numberFormatter)
                    .padding()
            }
            
            // Allow negatives, provide the button
            
            

        }
    }
}




struct AskForNumberRangeInputSheetView: View {
    var numberInput: InputAskForNumber
    @Binding var numberField: Double
    var range: ClosedRange<Double>
    var step: Double
    
    var body: some View {
        Form {
            Section(header: Text(numberInput.title ?? "No Current Input")) {
                Text("\(numberInput.order)")
                    .font(.caption)
            }
            
            if numberInput.promptBool == true {
                Section {
                    Text(numberInput.promptString ?? "Prompt here")
                }
            }
            
            Section {
                Slider(value: $numberField, in: range, step: step)
                Text(numberInput.allowDecimals ? "\(numberField, specifier: "%.2f")" : "\(Int(numberField))")
            }
        }
    }
}
