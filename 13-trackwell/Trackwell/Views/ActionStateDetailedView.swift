//
//  ActionStateDetailedView.swift
//  Trackwell
//
//  Created by Zachary Sturman on 8/25/23.
//



import SwiftUI

struct ActionStateDetailedView: View {
    @ObservedObject var vm: ActionStateDetailedViewModel
    @Environment(\.presentationMode) var presentationMode

    var body: some View {
        NavigationStack {
            VStack {
                List {
                    ForEach(vm.actionState.executions, id: \.id) { execution in
                        NavigationLink(destination: ExecutionDetailedView(execution: execution)) {
                            Text("Execution for trigger: \(execution.trigger.type.rawValue) at \(execution.timestamp)")
                        }
                    }
                }

                Text(vm.actionState.isAction ? "Action" : "State")
                
                // EXECUTION //
                HStack {
                    ForEach(vm.actionState.triggers, id: \.id) { trigger in
                        Button(action: {
                            vm.startProcessingInputs(for: trigger)
                        }, label: {
                            Text(trigger.type.rawValue)
                        })
                        .padding()
                        .background(Color.blue)
                        .foregroundColor(.white)
                        .cornerRadius(8)
                    }
                }

                
                Button("Edit") {
                    vm.showEditView.toggle()
                }
                .sheet(isPresented: $vm.showEditView) {
                    CreateEditActionStateView(vm: CreateEditActionStateViewModel(actionStateListVM: vm.actionStateListVM, editingActionState: vm.actionState))

                }

            }
            .navigationTitle(vm.actionState.title)
            .toolbar {
                ToolbarItem(placement: .navigationBarTrailing) {
                    Button(action: {
                        vm.deleteActionState {
                            presentationMode.wrappedValue.dismiss()
                        }
                    },
                    label: {
                        Image(systemName: "trash")
                    })
                }
            }


            // EXECUTION //
            .sheet(isPresented: $vm.showTextInputSheet, onDismiss: vm.processNextInput) {
                AskForTextInputView(inputValue: $vm.textInputValue, currentInputIndex: $vm.currentInputIndex, showTextInputSheet: $vm.showTextInputSheet)
                    .presentationDetents([.fraction(0.50), .fraction(0.80)])
                    .presentationDragIndicator(.visible)
            }
            
            // EXECUTION //
            .sheet(isPresented: $vm.showNumberInputSheet, onDismiss: vm.processNextInput) {
                AskForNumberInputSheet(showNumberInputSheet: $vm.showNumberInputSheet, currentInputIndex: $vm.currentInputIndex)
                    .presentationDetents([.fraction(0.20), .fraction(0.40), .fraction(0.60), .fraction(0.80)])
                    .presentationDragIndicator(.hidden)
            }
            
            // Alerts for Date, Location, SetText, SetNumber, Calculate and Error
            // !!!!!!!!
            // ADD executionNotificationContent from ActionStateDetailedViewModel based on the inputRequired = false
            
            // EXECUTION //
            .sheet(isPresented: $vm.showExecutionNotification, content: {
                //ExecutingInputSheet(currentInput: vm.currentInput<Input>)
                Text("Current input done")
            })
            
            
            // EXECUTION //
            .sheet(isPresented: $vm.showDateInputSheet, onDismiss: vm.processNextInput) {
                DateInputSheet(showDateInputSheet: $vm.showDateInputSheet, currentInputIndex: $vm.currentInputIndex)
                    .presentationDetents([.medium, .large])
            }
            // EXECUTION //
            .sheet(isPresented: $vm.showLocationInputSheet, onDismiss: vm.processNextInput) {
                LocationInputSheet(showLocationInputSheet: $vm.showLocationInputSheet, currentInputIndex: $vm.currentInputIndex)
                    .presentationDetents([.fraction(0.20), .fraction(0.40), .fraction(0.60), .fraction(0.80)])
                    .presentationDragIndicator(.visible)
            }
//            .alert(isPresented: $vm.showExecutionAlert) {
//                Alert(title: Text("Execution Created"), message: Text("A new execution has been created."), dismissButton: .default(Text("OK")))
//            }
        }
    }
}


