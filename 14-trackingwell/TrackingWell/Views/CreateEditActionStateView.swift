//
//  CreateEditActionStateView.swift
//  TrackingWell
//
//  Created by Zachary Sturman on 8/30/23.
//

import SwiftUI

struct CreateEditActionStateView: View {
    @ObservedObject var viewModel: CreateEditActionStateViewModel
    
    @Environment(\.dismiss) private var dismiss
    
    @State private var showTriggerOptions = false
    
    @State private var triggerNames: [String] = []
    @State private var inputDescriptions: [[String]] = []

    var body: some View {
        NavigationView {
            Form {
                GeneralInfo(isAction: $viewModel.isAction, title: $viewModel.title)

                
                Section(header: Text("Triggers")) {
                    ForEach(0..<triggerNames.count, id: \.self) { triggerIndex in
                        TriggerRowView(triggerName: $triggerNames[triggerIndex])
                        
                        ForEach(0..<inputDescriptions[triggerIndex].count, id: \.self) { inputIndex in
                            InputRowView(inputDescription: $inputDescriptions[triggerIndex][inputIndex])
                        }
                        
                        Button("Add Input") {
                            inputDescriptions[triggerIndex].append("")
                        }
                    }
                    
                }
                
                Button("Save") {
                    saveActionState()
                }
                Button("Add Trigger") {
                    showTriggerOptions.toggle()
                }
                .sheet(isPresented: $showTriggerOptions) {
                    TriggerOptionsView(selectedTriggers: $viewModel.selectedTriggers)
                        .presentationDragIndicator(.visible)
                }
                .sheet(item: $viewModel.currentTriggerBeingEdited) { trigger in
                    InputOptionsView(inputsForTrigger: self.viewModel.binding(for: trigger), currentTrigger: trigger)
                        .presentationDragIndicator(.visible)
                }
            }
            .navigationTitle(viewModel.isEditMode ? "Update ActionState" : "New ActionState" )
            .toolbar {
                ToolbarItem(placement: .navigationBarLeading) {
                    Button("Cancel") {
                        dismiss()
                    }
                }
                ToolbarItem(placement: .navigationBarTrailing) {
                    Button("Save") {
                        viewModel.actionState.title = viewModel.title
                        viewModel.actionState.isAction = viewModel.isAction
                        viewModel.actionState.triggers = viewModel.selectedTriggers.map { triggerOption in
                            let trigger = Trigger(type: triggerOption)
                            let inputsForCurrentTrigger = viewModel.inputsForTriggers[triggerOption] ?? []

                            trigger.inputs = inputsForCurrentTrigger
                            return trigger
                        }
//                        if let existingIndex = vm.actionStateListVM.actionStates.firstIndex(where: { $0.id == vm.actionState.id }) {
//                            vm.actionStateListVM.actionStates[existingIndex] = vm.actionState
//                        } else {
//                            vm.actionStateListVM.actionStates.append(vm.actionState)
//                        }
                        dismiss()
                    }
                    
                }
            }
        }
    }
    
    func saveActionState() {
        // Iterate over the triggerNames and create new triggers
        for (triggerIndex, triggerName) in triggerNames.enumerated() {
            viewModel.createNewTrigger(title: triggerName)
            
            // For each trigger, iterate over its inputs and create new inputs
            for (inputIndex, inputDescription) in inputDescriptions[triggerIndex].enumerated() {
                viewModel.createNewInput(title: inputDescription, order: Int32(inputIndex), for: viewModel.triggers[triggerIndex])
            }
        }
        
        // Use the viewModel to save the created entities to CoreData
        viewModel.saveToCoreData()
        
        // Dismiss the view
        dismiss()
    }

}

struct GeneralInfo: View {
    @Binding var isAction: Bool
    @Binding var title: String
    
    var body: some View {
        Section {
            Picker("Choose Type", selection: $isAction) {
                Text("Action").tag(true)
                Text("State").tag(false)
            }
            .pickerStyle(SegmentedPickerStyle())
        }
        
        Section {
            TextField("Title", text: $title)
        }
    }
}
