//
//  InputRowCalculate.swift
//  BeingAnalytics
//
//  Created by Zachary Sturman on 9/12/23.
//


import SwiftUI

struct InputRowCalculate: View {
    @ObservedObject var vm: CreateActionStateVM
    var trigger: TempTrigger
    @Binding var input: TempInput
    @State var showCalculationSheet: Bool = false
    @State var shouldDismiss: Bool = false
    
    var body: some View {
        ZStack {
            VStack {
                List {
                    LabeledContent(content: {
                        Text("\(input.numberValue)")
                    }, label: {
                        Text("Number Value")
                    })
                    
                    LabeledContent(content: {
                        Text("\(input.valueOne ?? 999)")
                    }, label: {
                        Text("Value One")
                    })
                    
                    LabeledContent(content: {
                        Text("\(input.valueTwo ?? 999)")
                    }, label: {
                        Text("Value Two")
                    })
                    
                    LabeledContent(content: {
                        if input.valueOneIsInput == true {
                            Text("True")
                        } else {
                            Text("False")
                        }
                    }, label: {
                        Text("Value One is Input")
                    })
                    
                    LabeledContent(content: {
                        if input.valueTwoIsInput == true {
                            Text("True")
                        } else {
                            Text("False")
                        }
                    }, label: {
                        Text("Value Two is Input")
                    })
                    
                    
                    LabeledContent(content: {
                        Text("\(input.selectedInputOne?.uuidString ?? "No input 1")")
                    }, label: {
                        Text("Input number 1:")
                    })
                    
                    
                    LabeledContent(content: {
                        Text("\(input.selectedInputTwo?.uuidString ?? "No input 2")")
                    }, label: {
                        Text("Input number 2:")
                    })
                    
                }
                

                Button(action: {
                    showCalculationSheet.toggle()
                }, label: {
                    Text("Edit")
                })
                .buttonStyle(PlainButtonStyle())

            }
            .onAppear() {
                self.input = vm.updateCalculationValues(for: input)
            }

            .sheet(isPresented: $showCalculationSheet) {
                InputSheetCalculate(vm: vm, showCalculationSheet: $showCalculationSheet, shouldDismissParent: $shouldDismiss, tempCalculate: $input, isEditing: true)
            }
        }
    }
}
