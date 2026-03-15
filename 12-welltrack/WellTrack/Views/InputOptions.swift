//
//  InputOptions.swift
//  WellTrack
//
//  Created by Zachary Sturman on 8/20/23.
//

import SwiftUI
import CoreData

struct SelectTriggerView: View {
    @Environment(\.presentationMode) var presentationMode
    @ObservedObject var vm: ActionStateViewModel
    @Binding var selectTriggerSheet: Bool
    
    let inputTriggerArray: [String] = ["Button", "Date"]
    
    var body: some View {
        ScrollView {
            Text("\(vm.parentTrigger?.title ?? "No parent Trigger selected")")
            Section(header: Text("Triggers")) {
                ForEach(inputTriggerArray, id: \.self) { trigger in
                    InputOptionHStack(triggerInput: trigger)
                        .onTapGesture {
                            handleTriggerSelection(trigger: trigger)
                        }
                }
            }
        }
        .padding()
        .navigationTitle("Input Options")
        .toolbar {
            ToolbarItem(placement: .navigationBarTrailing) {
                Button(action: {
                    presentationMode.wrappedValue.dismiss()
                }, label: {
                    Image(systemName: "xmark.circle.fill")
                })
                .foregroundColor(.secondary)
            }
        }
    }
    
    
    func handleTriggerSelection(trigger: String) {
        _ = vm.createButtonTrigger()
        presentationMode.wrappedValue.dismiss()
    }

}

struct SelectInputView: View {
    @Environment(\.presentationMode) var presentationMode
    @ObservedObject var vm: ActionStateViewModel
    @Binding var selectInputSheet: Bool
    
    let inputOptionsArray: [String] = ["Ask for Text", "Ask for Number", "Set Text", "Set Number", "Calculate"]
    
    
    var body: some View {
        ScrollView {
            Text("\(vm.parentTrigger?.title ?? "No parent Trigger selected")")
            Section(header: Text("Variable Inputs")) {
                ForEach(inputOptionsArray, id: \.self) { input in
                    InputOptionHStack(triggerInput: input)
                        .onTapGesture {
                            handleInputSelection(input: input)
                        }

                }
            }
        }
        .padding()
        .navigationTitle("Input Options")
        .toolbar {
            ToolbarItem(placement: .navigationBarTrailing) {
                Button(action: {
                    presentationMode.wrappedValue.dismiss()
                }, label: {
                    Image(systemName: "xmark.circle.fill")
                })
                .foregroundColor(.secondary)
            }
        }
    }
    

    
    func handleInputSelection(input: String) {
        switch input {
        case "Ask for Text":
            _ = vm.askForTextInput()
        case "Ask for Number":
            _ = vm.askForNumberInput()
        case "Set Text":
            _ = vm.setTextInput()
        case "Set Number":
            _ = vm.setNumberInput()
        case "Calculate":
            _ = vm.calculateInput()
        default:
            break
        }
        presentationMode.wrappedValue.dismiss()
    }
}

struct InputOptionHStack: View {
    
    var triggerInput: String
    
    var body: some View {
        HStack {
            Text("\(triggerInput)")
            Spacer()
        }
        .padding()
        .background(Color.gray.opacity(0.1))
        .cornerRadius(10)
    }
}

struct AskForTextInputView: View {
    var input: Input
    
    @State var allowBlank: Bool = true
    @State var provideDefault: Bool = false
    @State var defaultValue: String = ""
    
    @State var isOpen: Bool = false
    
    var body: some View {
        DisclosureGroup(input.title, isExpanded: $isOpen) {
            Toggle(
                isOn: $allowBlank,
                label: {
                    Text("Allow blank")
                })
            Toggle(
                isOn: $provideDefault,
                label: {
                    Text("Provide default")
                })
            TextField(
                text: $defaultValue,
                label: {
                    Text("Enter default value")
                })
            // make invisible until toggled
            .disabled(!provideDefault)
        }
        
    }
}

struct AskForNumberInputView: View {
    var input: Input
    
    @State var allowDecimals: Bool = true
    @State var allowNegatives: Bool = true
    
    @State var isOpen: Bool = false
    
    var body: some View {
        DisclosureGroup(input.title, isExpanded: $isOpen)  {
            Toggle(
                isOn: $allowDecimals,
                label: {
                   Text( "Allow Decimals")
                }
            )
            Toggle(
                isOn: $allowNegatives,
                label: {
                   Text( "Allow Negatives")
                }
            )
        }
    }
}

struct SetTextInputView: View {
    var input: Input
    
    @State var setTextValue: String = "Text Value"
    @State var isOpen: Bool = true
    
    var body: some View {
        DisclosureGroup(input.title, isExpanded: $isOpen)  {
            Text("\(setTextValue)")
            TextField("Enter text", text: $setTextValue)
        }
    }
}

struct SetNumberInputView: View {
    var input: Input
    
    @State var setNumberValue: String = "0"
    @State var isOpen: Bool = true
    
    var body: some View {
        DisclosureGroup(input.title, isExpanded: $isOpen)  {
            Text("\(setNumberValue)")
            TextField("Enter number", text: $setNumberValue)
        }
    }
}

struct CalculateInputView: View {
    var input: Input
    
    @State var setTextValue: String = ""
    @State var operation: String = "+"
    
    @State var isOpen: Bool = true
    
    var body: some View {
        DisclosureGroup(input.title, isExpanded: $isOpen)  {
            TextField("Enter text", text: $setTextValue)
        }
    }
}








//struct InputOptions_Previews: PreviewProvider {
//    static var previews: some View {
//        InputOptionsListView()
//    }
//}
