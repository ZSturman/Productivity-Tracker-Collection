//
//  CreateActionStateView.swift
//  ActionStateExecution
//
//  Created by Zachary Sturman on 7/27/23.
//

import SwiftUI
import CoreData

struct CreateActionStateView: View {
    @ObservedObject var actionStateViewModel: ActionStateViewModel
    @Environment(\.presentationMode) var presentationMode
    
    @State private var isShowingNewFieldView = false
    @State private var showingError = false
    @State private var errorMessage = ""
    
    @State private var fields: [InputFieldVariables] = []
    @State private var fieldBeingEdited: InputFieldVariables?
    @State private var indexBeingEdited: Int?
    
    var categories = ["Action", "State"]
    
    var body: some View {
        
        Form {
            Section {
                Picker("Type", selection: $actionStateViewModel.actionStateCategory) {
                    ForEach(categories, id: \.self) {
                        Text($0)
                    }
                }
                .pickerStyle(SegmentedPickerStyle())
            }
            
            Section {
                TextField("Action State Name", text: $actionStateViewModel.actionStateName)
                TextField("Description", text: $actionStateViewModel.explanation)
            }
            
            
            Section {
                Toggle(isOn: $actionStateViewModel.collectDate) {
                    Text("Collect Date")
                }
                Toggle(isOn: $actionStateViewModel.collectTime) {
                    Text("Collect Time")
                }
                Toggle(isOn: $actionStateViewModel.collectLocation) {
                    Text("Collect Location")
                }
            }
            
            
            Section(
                footer: fields.count > 1 ? Text("Hold and drag to change order of inputs") : nil
            ) {
                ForEach(0..<fields.count, id: \.self) { index in
                    HStack {
                        Text(fields[index].name)
                        Spacer()
                    }
                    .contentShape(Rectangle())
                    .onTapGesture {
                        self.indexBeingEdited = index
                        self.fieldBeingEdited = fields[index]
                        self.isShowingNewFieldView = true
                    }
                }
                .onMove(perform: moveField)
                .onDelete(perform: deleteField)
            }
            
            Section(footer: Text("Manual input for specific use case")) {
                Button(
                    action: {
                        self.fieldBeingEdited = nil
                        self.isShowingNewFieldView = true
                    },
                    label: {
                        Text("Add Input +")
                    })
            }
        }
        .navigationTitle("New ActionState")
        .navigationBarTitleDisplayMode(.inline)
        .toolbar {
            ToolbarItem(placement: .navigationBarTrailing) {
                Button(action: {
                    createActionState()
                }) {
                    Text("Done")
                }
            }
        }
        .alert(isPresented: $showingError) {
            Alert(
                title: Text("Error"),
                message: Text(errorMessage),
                dismissButton: .default(Text("OK"))
            )
        }
        .sheet(isPresented: $isShowingNewFieldView) {
            NewInputFields(field: self.fieldBeingEdited) { newField in
                  if let index = self.indexBeingEdited {
                      self.fields[index] = newField
                  } else {
                      self.fields.append(newField)
                  }
                  self.indexBeingEdited = nil
              }
        }
    }
    
    private func moveField(from source: IndexSet, to destination: Int) {
        fields.move(fromOffsets: source, toOffset: destination)
    }
    
    private func deleteField(at offsets: IndexSet) {
        fields.remove(atOffsets: offsets)
    }
    
    
    private func createActionState() {
        let result = actionStateViewModel.createActionState(fields: fields)
        switch result {
        case .success:
            presentationMode.wrappedValue.dismiss()
        case .failure(let error):
            errorMessage = "Error: \(error.localizedDescription)"
            showingError = true
        }
    }
}
