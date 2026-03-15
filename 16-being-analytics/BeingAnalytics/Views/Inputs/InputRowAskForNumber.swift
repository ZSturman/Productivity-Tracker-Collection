//
//  InputRowAskForNumber.swift
//  BeingAnalytics
//
//  Created by Zachary Sturman on 9/12/23.
//

import SwiftUI
import Combine


struct InputRowAskForNumber: View {
    
    @Binding var promptBool: Bool
    @Binding var promptString: String
    @Binding var useRange: Bool
    @Binding var currency: Bool
    @Binding var allowNegatives: Bool
    @Binding var allowDecimals: Bool
    @Binding var defaultNumberValue: Double
    @Binding var stepCount: Double
    @Binding var minNumberValue: Double
    @Binding var maxNumberValue: Double
    
    @State private var showAlert: Bool = false
    @State private var alertTitle: String = ""
    @State private var alertMessage: String = ""
    
    let numberFormatter: NumberFormatter = {
        let formatter = NumberFormatter()
        formatter.numberStyle = .decimal
        formatter.minimumFractionDigits = 2
        formatter.maximumFractionDigits = 2
        return formatter
    }()
    
    var body: some View {
        HStack {
            Image(systemName: "ellipsis.message")
                .foregroundColor(.gray)
                .font(.headline)
            Toggle(isOn: $promptBool, label: {
                Text("Display prompt?")
            })
        }
        
        if promptBool {
            HStack {
                Image(systemName: "textformat")
                    .foregroundColor(.gray)
                    .font(.headline)
                TextField("Enter text value...", text: $promptString)
            }
            .padding()
            .overlay(RoundedRectangle(cornerRadius: 10).stroke(Color.gray, lineWidth: 1))
        }
        
        HStack {
            Image(systemName: "plus.forwardslash.minus")
                .foregroundColor(.gray)
                .font(.headline)
            Toggle(isOn: $allowNegatives, label: {
                Text("Allow negatives?")
            })
        }
        
        HStack {
            Image(systemName: "numbersign")
                .foregroundColor(.gray)
                .font(.headline)
            Toggle(isOn: $allowDecimals, label: {
                Text("Allow decimals?")
            })
        }
        
        HStack {
            Image(systemName: "arrowtriangle.left.and.line.vertical.and.arrowtriangle.right")
                .foregroundColor(.gray)
                .font(.headline)
            Toggle(isOn: $useRange, label: {
                Text("Select from range of values?")
            })
        }
        
        if useRange {
                    HStack {
                        Image(systemName: "minus.circle")
                            .foregroundColor(.gray)
                            .font(.headline)
                        Text("Minimum Value:")
                        Spacer()
                        NumberField(placeholder: "Min Value", value: $minNumberValue, allowDecimals: allowDecimals)
                            .keyboardType(.decimalPad)
                    }
                    .padding()
                    .overlay(RoundedRectangle(cornerRadius: 10).stroke(Color.gray, lineWidth: 1))
                    
                    HStack {
                        Image(systemName: "plus.circle")
                            .foregroundColor(.gray)
                            .font(.headline)
                        Text("Maximum Value:")
                        Spacer()
                        NumberField(placeholder: "Max Value", value: $maxNumberValue, allowDecimals: allowDecimals)
                            .keyboardType(.decimalPad)
                    }
                    .padding()
                    .overlay(RoundedRectangle(cornerRadius: 10).stroke(Color.gray, lineWidth: 1))
                    
                    HStack {
                        Image(systemName: "stairs")
                            .foregroundColor(.gray)
                            .font(.headline)
                        Text("Step Count:")
                        Spacer()
                        NumberField(placeholder: "Step Count", value: $stepCount, allowDecimals: allowDecimals)
                            .keyboardType(.decimalPad)
                    }
                    .padding()
                    .overlay(RoundedRectangle(cornerRadius: 10).stroke(Color.gray, lineWidth: 1))
                }
                
                HStack {
                    Image(systemName: "number.circle")
                        .foregroundColor(.gray)
                        .font(.headline)
                    Text("Default Value:")
                    Spacer()
                    NumberField(placeholder: "Enter default value", value: $defaultNumberValue, allowDecimals: allowDecimals)
                        .keyboardType(allowDecimals ? .decimalPad : .numberPad)
                }
                .padding()
                .overlay(RoundedRectangle(cornerRadius: 10).stroke(Color.gray, lineWidth: 1))
            }
    
    
    func formatNumber(_ value: Double) -> String {
            return allowDecimals ? String(format: "%.2f", value) : "\(Int(value))"
        }
}


struct NumberField: View {
    @Binding var value: Double
    var placeholder: String
    var allowDecimals: Bool
    
    @State private var stringValue: String
    
    init(placeholder: String, value: Binding<Double>, allowDecimals: Bool = true) {
        self.placeholder = placeholder
        self._value = value
        self.allowDecimals = allowDecimals
        _stringValue = State(initialValue: String(value.wrappedValue))
    }
    
    var body: some View {
        TextField(placeholder, text: $stringValue, onCommit: validateInput)
            .keyboardType(allowDecimals ? .decimalPad : .numberPad)
            .onChange(of: stringValue) { newValue in
                validateInput()
            }
    }
    
    private func validateInput() {
        if let newValue = Double(stringValue), (allowDecimals || floor(newValue) == newValue) {
            value = newValue
        } else {
            stringValue = String(value)
        }
    }
}
