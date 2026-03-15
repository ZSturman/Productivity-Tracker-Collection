//
//  InputRowView.swift
//  BeingAnalytics
//
//  Created by Zachary Sturman on 9/1/23.
//


import SwiftUI

struct InputRowView: View {
    var trigger: TempTrigger
    @Binding var input: TempInput
    @ObservedObject var vm: CreateActionStateVM
    
    @State private var isRowExpanded: Bool
    
    // Initialize the expansion state using the getLocation property
    init(trigger: TempTrigger, input: Binding<TempInput>, vm: CreateActionStateVM) {
        self.trigger = trigger
        self._input = input
        self.vm = vm
        
        // Step 2: Initialize using getLocation
        self._isRowExpanded = State(initialValue: input.wrappedValue.inputRowExpanded)
    }
    
    var body: some View {

        VStack(alignment: .leading) {
                
                DisclosureGroup(isExpanded: $isRowExpanded, content: {
                    if input.inputType == .askForText {
                        InputRowAskForText(promptBool: $input.promptBool, allowBlank: $input.allowBlank, defaultBool: $input.defaultBool, promptString: $input.promptString, defaultString: $input.defaultString)
                    } else if input.inputType == .askForNumber {
                        InputRowAskForNumber(promptBool: $input.promptBool, promptString: $input.promptString, useRange: $input.useRange, currency: $input.currency, allowNegatives: $input.allowNegatives, allowDecimals: $input.allowDecimals, defaultNumberValue: $input.defaultNumberValue, stepCount: $input.stepCount, minNumberValue: $input.minNumberValue, maxNumberValue: $input.maxNumberValue)
                    } else if input.inputType == .currentDatetime {
                        InputRowCurrentDatetime(collectDate: $input.date, collectTime: $input.time)
                    } else if input.inputType == .getLocation {
                        InputRowGetLocation()
                    } else if input.inputType == .setText {
                        InputRowSetText(setValue: $input.setValue)
                    } else if input.inputType == .setNumber {
                        InputRowSetNumber(vm: vm, trigger: trigger, currency: $input.currency, setValueDouble: $input.numberValue)
                    } else if input.inputType == .calculate {
                        InputRowCalculate(vm: vm, trigger: trigger, input: $input)
                    }
                }, label: {
                    HStack {
                        Image(systemName: input.inputSystemImage)
                            .foregroundColor(.gray)
                            .font(.headline)
                            .opacity(0.5)
                        Text("(\(input.order))")
                            .opacity(0.7)
                        Text(input.title)
                    }
                })
                


                Text("Index: \(input.order)")
                    .font(.caption)
            }
        }
    }
//}
