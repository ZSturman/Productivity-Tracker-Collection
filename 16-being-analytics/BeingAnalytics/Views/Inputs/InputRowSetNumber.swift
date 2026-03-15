//
//  InputRowSetNumber.swift
//  BeingAnalytics
//
//  Created by Zachary Sturman on 9/12/23.
// 

import SwiftUI

struct InputRowSetNumber: View {
    @ObservedObject var vm: CreateActionStateVM
    var trigger: TempTrigger
    @Binding var currency: Bool
    @Binding var setValueDouble: Double
    
    init(vm: CreateActionStateVM, trigger: TempTrigger, currency: Binding<Bool>, setValueDouble: Binding<Double>) {
        self.vm = vm
        self.trigger = trigger
        _currency = currency
        _setValueDouble = setValueDouble
    }
    
    let numberFormatter: NumberFormatter = {
        let formatter = NumberFormatter()
        formatter.numberStyle = .decimal
        formatter.minimumFractionDigits = 0
        formatter.maximumFractionDigits = 10
        return formatter
    }()
    
    let numberCurrencyFormatter: NumberFormatter = {
        let formatter = NumberFormatter()
        formatter.numberStyle = .decimal
        formatter.minimumFractionDigits = 2
        formatter.maximumFractionDigits = 2
        return formatter
    }()
    
    var body: some View {
        VStack {
            HStack {
                Image(systemName: "dollarsign")
                    .foregroundColor(.gray)
                    .font(.headline)
                Toggle(isOn: $currency, label: {
                    Text("Currency?")
                })
            }
            if currency {
                HStack {
                    Image(systemName: "dollarsign")
                        .foregroundColor(.gray)
                        .font(.headline)
                    TextField("Enter response...", value: $setValueDouble, formatter: numberCurrencyFormatter)
                        .onChange(of: setValueDouble) { newValue in
                            vm.updateTriggerValue(for: trigger.id, newValue: newValue)
                        }

                }
                .padding()
                .overlay(RoundedRectangle(cornerRadius: 10).stroke(Color.gray, lineWidth: 1))
                .keyboardType(.decimalPad)
            } else {
                HStack {
                    Image(systemName: "number")
                        .foregroundColor(.gray)
                        .font(.headline)
                    TextField("Enter response...", value: $setValueDouble, formatter: numberFormatter)
                        .onChange(of: setValueDouble) { newValue in
                            vm.updateTriggerValue(for: trigger.id, newValue: newValue)
                        }

                }
                .padding()
                .overlay(RoundedRectangle(cornerRadius: 10).stroke(Color.gray, lineWidth: 1))
                .keyboardType(.decimalPad)
            }
        }

        
    }
}
