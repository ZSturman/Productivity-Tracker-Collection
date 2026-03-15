//
//  CreateEditActionState.swift
//  WellTrack
//
//  Created by Zachary Sturman on 8/15/23.
//

import SwiftUI

enum Category: String, CaseIterable, Identifiable {
    case action = "Action"
    case state = "State"

    var id: String { rawValue }
}

enum ValidationError: Identifiable {
    case titleBlank
    case categoryNotSelected

    var id: Int {
        switch self {
            case .titleBlank: return 1
            case .categoryNotSelected: return 2
        }
    }
}




struct CreateEditActionState: View {
    @Environment(\.dismiss) private var dismiss
    @ObservedObject var vm: ActionStateViewModel
    @State private var hasError: Bool = false
    @State var selectInputSheet: Bool = false
    @State var selectTriggerSheet: Bool = false
    @State private var currentError: ValidationError?

    var body: some View {
        Form {
            GeneralSection(selectedCategory: $vm.actionState.category, title: $vm.actionState.title, collectLocation: $vm.actionState.collectLocation)
            
            ForEach(vm.triggersArray, id: \.id) { trigger in
                
                Section(
                    content: {
                        DisclosureGroup(trigger.title) {
                            VStack{
                                Text("Heres where the parameters and stuff will go")
                                Text("More params")
                            }
                        }
                        ForEach(vm.inputsArray.filter { $0.parentTrigger == trigger }, id: \.id) { input in
                            if input.inputType == "AskForTextInput" {
                                AskForTextInputView(input: input)
                            }
                            if input.inputType == "AskForNumberInput" {
                                AskForNumberInputView(input: input)
                            }
                            if input.inputType == "SetTextInput" {
                                SetTextInputView(input: input)
                            }
                            if input.inputType == "SetNumberInput" {
                                SetNumberInputView(input: input)
                            }
                            if input.inputType == "CalculateInput" {
                                CalculateInputView(input: input)
                            }
                        }
                        Button(action: {
                            selectTriggerSheet = false
                            vm.parentTrigger = trigger
                            selectInputSheet = true
                            
                        }) {
                            HStack {
                                Image(systemName: "plus.circle")
                                Text("Add Input")
                            }
                        }
                    },
                    footer: {
                        Text("this is a footer")
                    })
            }
                Button(action: {
                    selectInputSheet = false
                    vm.parentTrigger = nil
                    selectTriggerSheet = true
                }) {
                    HStack {
                        Image(systemName: "plus.circle")
                        Text("Add Trigger")
                    }
                }
        
            OutputListView(vm: vm)
        }
        .navigationTitle(vm.isNew ? "New ActionState" : "Update ActionState")
        .sheet(isPresented: $selectInputSheet) {
            NavigationStack {
                SelectInputView(vm: vm, selectInputSheet: $selectInputSheet)
            }
        }
        .sheet(isPresented: $selectTriggerSheet) {
            NavigationStack {
                SelectTriggerView(vm: vm, selectTriggerSheet: $selectTriggerSheet)
            }
        }
        .toolbar {
            ToolbarItem(placement: .confirmationAction) {
                Button("Done") {
                    validate()
                }
            }
            ToolbarItem(placement: .navigationBarLeading) {
                Button("Cancel") {
                    dismiss()
                }
            }
        }
        .alert(item: $currentError) { error in
            switch error {
            case .titleBlank:
                return Alert(title: Text("Error"), message: Text("Title cannot be blank"), dismissButton: .default(Text("OK")))
            case .categoryNotSelected:
                return Alert(title: Text("Error"), message: Text("Please select a category"), dismissButton: .default(Text("OK")))
            }
        }
    }
    

}




struct AddInputButton: View {
    @Binding var selectInputSheet: Bool
    var addText: String = "Input Option"
    
    
    var body: some View {
        Button(action: {
            selectInputSheet = true
        }) {
            HStack {
                Image(systemName: "plus.circle")
                Text("Add \(addText)")
            }
        }
    }
}

struct AddTriggerButton: View {
    @Binding var selectTriggerSheet: Bool
    var addText: String = "Trigger Option"
    
    var body: some View {
        Button(action: {
            selectTriggerSheet = true
        }) {
            HStack {
                Image(systemName: "plus.circle")
                Text("Add \(addText)")
            }
        }
    }
}











struct GeneralSection: View {
    @Binding var selectedCategory: String
    @Binding var title: String
    @Binding var collectLocation: Bool

    var body: some View {
        Section {
            Picker("Select a Category", selection: $selectedCategory) {
                ForEach(Category.allCases, id: \.self) { category in
                    Text(category.rawValue).tag(category.rawValue)
                }
            }
            .pickerStyle(SegmentedPickerStyle())
        }
        Section {
            TextField("Name", text: $title)
                .keyboardType(.namePhonePad)
        }
        Section {
            Toggle("Collect Location", isOn: $collectLocation)
        }
    }
}

struct InputRow: View {
    @ObservedObject var vm: ActionStateViewModel
    @Binding var selectTriggerSheet: Bool
    @Binding var selectInputSheet: Bool

    var body: some View {
        ForEach(vm.triggersArray, id: \.id) { trigger in
            Section {
                
                // Filtering the inputs based on the parentTrigger relationship
                ForEach(vm.inputsArray.filter { $0.parentTrigger == trigger }, id: \.id) { input in
                    Text("\(input.title)")
                }
                
                if let childInputs = trigger.childInputs?.allObjects as? [Input] {
                    Text("\(childInputs.count)")
                    if let firstInput = childInputs.first {
                        RecursiveInputView(input: firstInput, selectInputSheet: $selectInputSheet)
                    }
                }

            }
        }
        
        Section {
            AddTriggerButton(selectTriggerSheet: $selectTriggerSheet, addText: "Trigger")
        }
    }
}


struct RecursiveInputView: View {
    var input: Input
    @Binding var selectInputSheet: Bool

    var body: some View {
        VStack {
            Text("\(input.title)")

            if let nextInput = input.nextInput {
                RecursiveInputView(input: nextInput, selectInputSheet: $selectInputSheet)
            } else {
                AddInputButton(selectInputSheet: $selectInputSheet, addText: "Input")
            }
        }
    }
}




extension InputRow {
    func move(from source: IndexSet, to destination: Int) {
        vm.inputsArray.move(fromOffsets: source, toOffset: destination)
        updateOrderIndexes()
    }
    
    func updateOrderIndexes() {
        for (index, input) in vm.inputsArray.enumerated() {
            input.orderIndex = Int16(index)
        }
    }
}

extension InputRow {
    func delete(at offsets: IndexSet) {
        for index in offsets {
            let input = vm.inputsArray[index]
            vm.removeInput(input: input)
        }
        updateOrderIndexes()
    }
}










private extension CreateEditActionState {
    
    func validate() {
        print("DEBUG: Validating CreateEditActionState")
        
        if vm.actionState.title.isEmpty {
            print("DEBUG: ActionState title is empty")
            currentError = .titleBlank
            return
        }
        
        if vm.actionState.category.isEmpty {
            print("DEBUG: ActionState category is empty")
            currentError = .categoryNotSelected
            return
        }
        
        if let context = vm.actionState.managedObjectContext {
            print(context)
        } else {
            print("ActionState does not have an associated managed object context.")
        }

        if vm.actionState.isValid {
            print("DEBUG: ActionState is valid")
            vm.actionState.dateUpdated = Date()
            vm.addInput(inputs: vm.inputsArray)
            
            print("DEBUG: Inputs in vm.inputsArray: \(vm.inputsArray.map { $0.title })") // Assuming each input has a 'title' property.
                    
            // Handle nested relationships if any (like Triggers or Inputs)
            for trigger in vm.triggersArray {
                print("DEBUG: Processing trigger: \(trigger.title)") // Assuming each trigger has a 'title' property.
                trigger.dateUpdated = Date()

                if let childInputs = trigger.childInputs?.allObjects as? [Input] {
                    print("DEBUG: Child inputs for trigger \(trigger.title): \(childInputs.map { $0.title }) ")
                    
                    // Reset all isFirst properties to false
                    childInputs.forEach { $0.isFirst = false }
                    
                    // Set the first child input's isFirst property to true.
                    childInputs.first?.isFirst = true
                    
                    print("DEBUG: Child inputs for trigger \(trigger.title): \(childInputs.map { $0.isFirst }) ")
                    for input in childInputs {
                        input.dateUpdated = Date()
                    }
                } else {
                    print("DEBUG: No child inputs for trigger \(trigger.title) or failed to cast")
                }


            }


            do {
                try vm.save()
                dismiss()
            } catch {
                print(error)
            }
        } else {
            hasError = true
        }
    }
}








struct CreateEditActionState_Previews: PreviewProvider {
    static var previews: some View {
        NavigationStack {
            let preview = ActionStateDataController.shared
            CreateEditActionState(vm: .init(controller: preview))
                .environment(\.managedObjectContext, preview.viewContext)
        }
    }
}


