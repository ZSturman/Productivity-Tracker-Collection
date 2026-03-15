//
//  CreateEditActionStateView.swift
//  Trackwell
//
//  Created by Zachary Sturman on 8/25/23.
//
import SwiftUI

struct CreateEditActionStateView: View {
    @ObservedObject var vm: CreateEditActionStateViewModel
    @Environment(\.presentationMode) var presentationMode
    
    

    var body: some View {
        NavigationStack {
            Form {
                GeneralInfo(vm: vm)
                List {
                    ForEach(vm.selectedTriggers, id: \.self) { trigger in
                        Section(header: HStack {
                            Text(trigger.rawValue)
                            Spacer()
                            Button("Add Inputs") {
                                vm.currentTriggerBeingEdited = trigger
                            }
                            Button("Delete") {
                                vm.deleteTrigger(trigger)
                            }
                        }, footer: HStack {
                            if vm.inputsForTriggers.count > 0{
                                Text("Whatever the last input is")
                            } else {
                                Text("Output: Current Date")
                            }
                    
                                
                        }) {
                            ForEach(vm.inputsForTriggers[trigger.id] ?? [], id: \.id) { input in
                                switch input.type {
                                case .AskForText:
                                    AskForTextInputDisclosure(input: input)
                                case .AskForNumber:
                                    AskForNumberInputDisclosure(input: input)
                                case .Calculate:
                                    CalculateInputDisclosure(input: input)
                                case .SetText:
                                    SetTextInputDisclosure(input: input)
                                case .SetNumber:
                                    SetNumberInputDisclosure(input: input)
                                case .GetLocation:
                                    GetLocationtInputDisclosure(input: input)
                                case .Date:
                                    DateInputDisclosure(input: input)
                                }
                            }

                            .onDelete { offsets in
                                vm.deleteInput(forTrigger: trigger, at: offsets)
                            }
                            .onMove { source, destination in
                                vm.moveInput(forTrigger: trigger, from: source, to: destination)
                            }
                        }
                    }
                }
                Button("Add Trigger") {
                    vm.showTriggerOptions.toggle()
                }
                .sheet(isPresented: $vm.showTriggerOptions) {
                    TriggerOptionsView(selectedTriggers: $vm.selectedTriggers)
                        .presentationDragIndicator(.visible)
                }
                .sheet(item: $vm.currentTriggerBeingEdited) { trigger in
                    InputOptionsView(inputsForTrigger: self.vm.binding(for: trigger), currentTrigger: trigger)
                        .presentationDragIndicator(.visible)
                }
            }
            .navigationTitle(vm.isNew ? "New ActionState" : "Update ActionState")
            .toolbar {
                ToolbarItem(placement: .navigationBarLeading) {
                    Button("Cancel") {
                        presentationMode.wrappedValue.dismiss()
                    }
                }
                ToolbarItem(placement: .navigationBarTrailing) {
                    Button("Save") {
                        vm.actionState.title = vm.title
                        vm.actionState.isAction = vm.isAction
                        vm.actionState.triggers = vm.selectedTriggers.map { triggerOption in
                            let trigger = Trigger(type: triggerOption)
                            let inputsForCurrentTrigger = vm.inputsForTriggers[triggerOption] ?? []

                            trigger.inputs = inputsForCurrentTrigger
                            return trigger
                        }
                        if let existingIndex = vm.actionStateListVM.actionStates.firstIndex(where: { $0.id == vm.actionState.id }) {
                            vm.actionStateListVM.actionStates[existingIndex] = vm.actionState
                        } else {
                            vm.actionStateListVM.actionStates.append(vm.actionState)
                        }
                        presentationMode.wrappedValue.dismiss()
                    }
                    
                }
            }
        }
    }
    
    struct GeneralInfo: View {
        @ObservedObject var vm: CreateEditActionStateViewModel
        
        var body: some View {
            Section {
                Picker("Choose Type", selection: $vm.isAction) {
                    Text("Action").tag(true)
                    Text("State").tag(false)
                }
                .pickerStyle(SegmentedPickerStyle())
            }
            
            Section {
                TextField("Title", text: $vm.title)
            }
        }
    }

    struct RowItem: Identifiable {
        enum ItemType {
            case trigger(TriggerType)
            case input(TriggerType, Input)
        }

        let id = UUID()
        let type: ItemType
    }

    var allRows: [RowItem] {
        var rows: [RowItem] = []
        for trigger in vm.selectedTriggers {
            rows.append(RowItem(type: .trigger(trigger)))
            if let inputsForThisTrigger = vm.inputsForTriggers[trigger.type] {
                for input in inputsForThisTrigger {
                    rows.append(RowItem(type: .input(trigger, input)))
                }
            }
        }
        return rows
    }

}
