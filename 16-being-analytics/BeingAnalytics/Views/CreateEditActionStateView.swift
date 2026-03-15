//
//  CreateEditActionStateView.swift
//  BeingAnalytics
//
//  Created by Zachary Sturman on 9/1/23.
//

import SwiftUI

struct CreateEditActionStateView: View {
    @ObservedObject var vm: CreateActionStateVM
    @Environment(\.dismiss) private var dismiss
    
    @State var showAddTriggerSheet = false
    @State var showAddInputSheet = false
    @State var showCalculationSheet = false
    @State var shouldDismiss: Bool = false
    
    @State private var showingErrorAlert = false
    
    var body: some View {
        NavigationStack {
            ZStack {
                VStack {
                    Form {
                        GeneralInfoView(vm: vm)
    
                        SelectedTriggerListView(vm: vm, showAddInputSheet: $showAddInputSheet)
    
                        Button("+ Add Trigger") {
                            showAddTriggerSheet.toggle()
                        }
                    }
                }
                .sheet(isPresented: $showAddTriggerSheet) {
                    AddTriggerSheetView(vm: vm)
                }
                .sheet(isPresented: $showAddInputSheet) {
                    AddInputSheetView(vm: vm)
                }

            }
            .navigationTitle("Create ActionState")
            .toolbar {
                ToolbarItem(placement: .navigationBarTrailing) {
                    Button(action: {
                        if vm.saveNewActionState() {
                            dismiss()
                        }
                        // Optionally, you can show an error message or feedback to the user here.
                    }, label: {
                        Text("Save")
                    })

                }
                ToolbarItem(placement: .navigationBarLeading) {
                    Button(action: {
                        dismiss()
                    }, label: {
                        Text("Cancel")
                    })

                }
            }
            
            .alert(isPresented: $showingErrorAlert) {
                Alert(title: Text("Error"), message: Text(vm.errorMessage ?? "Unknown Error"), dismissButton: .default(Text("OK")))
            }
            .onChange(of: vm.errorMessage) { newValue in
                if newValue != nil {
                    showingErrorAlert = true
                }
            }
        }
        .onDisappear {
            // Fetch the updated ActionState or perform other actions needed when the view disappears.
            // For example, if you have a method in your ViewModel to fetch the updated ActionState, you can call it here.
            vm.dataService.fetchObjectByID(by: vm.newActionState.id, entityType: ActionState.self)
        }
    }
}



struct GeneralInfoView: View {
    
    @ObservedObject var vm: CreateActionStateVM
    
    @State private var internalSelectedCategory: String
    var actionOrState = ["Action", "State"]

    init(vm: CreateActionStateVM) {
        self.vm = vm
        _internalSelectedCategory = State(initialValue: vm.newActionState.isAction ? "Action" : "State")
    }
    
    var body: some View {
        Section {
            Picker("Select a Category", selection: $internalSelectedCategory) {
                ForEach(actionOrState, id: \.self) { descriptor in
                    Text(descriptor).tag(descriptor)
                }
            }
            .pickerStyle(SegmentedPickerStyle())
            .onChange(of: internalSelectedCategory) { newValue in
                vm.newActionState.isAction = (newValue == "Action")
            }
        }
        Section {
            TextField("Title", text: $vm.newActionState.title)
        }
    }
}
