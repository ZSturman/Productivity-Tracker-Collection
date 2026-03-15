//
//  InputOptionsView.swift
//  Trackwell
//
//  Created by Zachary Sturman on 8/26/23.
//

import SwiftUI

struct InputOptionsView: View {
    @Binding var inputsForTrigger: [Input]
    var currentTrigger: TriggerType
    @Environment(\.presentationMode) var presentationMode

    var body: some View {
        List(InputType.allCases, id: \.self) { option in
            Button(action: {
                inputsForTrigger.append(Input(type: option))

                presentationMode.wrappedValue.dismiss()
            }) {
                HStack {
                    Text(option.rawValue)
                    if option.requiresInput {
                        Spacer()
                        Image(systemName: "exclamationmark.circle")
                            .foregroundColor(.orange)
                    }
                }
            }
        }
    }
}

struct AskForTextInputDisclosure: View {
    @ObservedObject var input: Input

    @State var isOpen: Bool = true
    
    var body: some View {
        DisclosureGroup(input.type.rawValue, isExpanded: $isOpen) {
            Toggle(
                isOn: $input.allowBlank,
                label: {
                    Text("Allow blank")
                })
            Toggle(
                isOn: $input.provideDefault,
                label: {
                    Text("Provide default")
                })
            TextField(
                text: $input.defaultValue,
                label: {
                    Text("Enter default value")
                })
            .disabled(!input.provideDefault)
        }
    }
}


struct AskForNumberInputDisclosure: View {
    @ObservedObject var input: Input
    
    @State var allowBlank: Bool = true
    @State var provideDefault: Bool = false
    @State var defaultValue: String = ""
    
    @State var isOpen: Bool = true
    
    var body: some View {
        DisclosureGroup(input.type.rawValue, isExpanded: $isOpen) {
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



struct CalculateInputDisclosure: View {
    @ObservedObject var input: Input
    
    @State var allowBlank: Bool = true
    @State var provideDefault: Bool = false
    @State var defaultValue: String = ""
    
    @State var isOpen: Bool = true
    
    var body: some View {
        DisclosureGroup(input.type.rawValue, isExpanded: $isOpen) {
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

struct SetTextInputDisclosure: View {
    @ObservedObject var input: Input
    
    @State var allowBlank: Bool = true
    @State var provideDefault: Bool = false
    @State var defaultValue: String = ""
    
    @State var isOpen: Bool = true
    
    var body: some View {
        DisclosureGroup(input.type.rawValue, isExpanded: $isOpen) {
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



struct SetNumberInputDisclosure: View {
    @ObservedObject var input: Input
    
    @State var allowBlank: Bool = true
    @State var provideDefault: Bool = false
    @State var defaultValue: String = ""
    
    @State var isOpen: Bool = true
    
    var body: some View {
        DisclosureGroup(input.type.rawValue, isExpanded: $isOpen) {
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



struct GetLocationtInputDisclosure: View {
    @ObservedObject var input: Input
    
    @State var allowBlank: Bool = true
    @State var provideDefault: Bool = false
    @State var defaultValue: String = ""
    
    @State var isOpen: Bool = true
    
    var body: some View {
        DisclosureGroup(input.type.rawValue, isExpanded: $isOpen) {
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



struct DateInputDisclosure: View {
    @ObservedObject var input: Input
    
    @State var getDate: Bool = true
    @State var getTime: Bool = false
    
    @State var isOpen: Bool = false
    
    var body: some View {
        DisclosureGroup(input.type.rawValue, isExpanded: $isOpen) {
            Toggle(
                isOn: $getDate,
                label: {
                    Text("Date")
                })
            Toggle(
                isOn: $getTime,
                label: {
                    Text("Time")
                })
        }
    }
}


