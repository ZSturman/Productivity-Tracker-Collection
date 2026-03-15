//
//  InputExecutionViews.swift
//  Trackwell
//
//  Created by Zachary Sturman on 8/28/23.
// 

import SwiftUI

struct AskForTextInputView: View {
    @Binding var inputValue: String
    @Binding var currentInputIndex: Int
    @Binding var showTextInputSheet: Bool

    var body: some View {
        VStack {
            Text("\(currentInputIndex)")
            TextField("Enter Text", text: $inputValue)
                .padding()
                .background(Color.gray.opacity(0.2))
                .cornerRadius(8)
            Spacer()
            HStack {
                Button("Cancel") {
                    showTextInputSheet = false
                }
                .padding()
                .background(Color.red)
                .foregroundColor(.white)
                .cornerRadius(8)
                
                Button("Okay") {
                    showTextInputSheet = false
                }
                .padding()
                .background(Color.green)
                .foregroundColor(.white)
                .cornerRadius(8)
            }
        }
        .padding()
    }
}

struct AskForNumberInputSheet: View {
    @Binding var showNumberInputSheet: Bool
    @Binding var currentInputIndex: Int
    
    var body: some View {
        VStack {
            Text("This is for the Numbers!")
            Text("\(currentInputIndex)")
            HStack {
                Button("Cancel") {
                    showNumberInputSheet = false
                }
                .padding()
                .background(Color.red)
                .foregroundColor(.white)
                .cornerRadius(8)
                
                Button("Okay") {
                    showNumberInputSheet = false
                }
                .padding()
                .background(Color.green)
                .foregroundColor(.white)
                .cornerRadius(8)
            }
        }
    }
}

struct ExecutingInputSheet: View {
    @Binding var showExecutionNotification: Bool
    var currentInput: Input
    
    var body: some View {
        VStack {
            Text("\(currentInput.type.rawValue)")
            
        }
    }
}



struct LocationInputSheet: View {
    @Binding var showLocationInputSheet: Bool
    @Binding var currentInputIndex: Int
    
    var body: some View {
        VStack {
            Text("LOOOOOOOcation!")
            Text("\(currentInputIndex)")
            HStack {
                Button("Cancel") {
                    showLocationInputSheet = false
                }
                .padding()
                .background(Color.red)
                .foregroundColor(.white)
                .cornerRadius(8)
                
                Button("Okay") {
                    showLocationInputSheet = false
                }
                .padding()
                .background(Color.green)
                .foregroundColor(.white)
                .cornerRadius(8)
            }
        }
    }
}

struct DateInputSheet: View {
    @Binding var showDateInputSheet: Bool
    @Binding var currentInputIndex: Int
    
    var body: some View {
        VStack {
            Text("This is for the Date!")
                .font(.largeTitle)
            Text("\(currentInputIndex)")
            HStack {
                Button("Cancel") {
                    showDateInputSheet = false
                }
                .padding()
                .background(Color.red)
                .foregroundColor(.white)
                .cornerRadius(8)
                
                Button("Okay") {
                    showDateInputSheet = false
                }
                .padding()
                .background(Color.green)
                .foregroundColor(.white)
                .cornerRadius(8)
            }
        }
    }
}
