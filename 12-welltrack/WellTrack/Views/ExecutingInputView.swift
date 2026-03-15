//
//  ExecutingInputView.swift
//  WellTrack
//
//  Created by Zachary Sturman on 8/23/23.
//

import SwiftUI

struct ExecutingInputView: View {
    @ObservedObject var vm: ActionStateViewModel
    @State var askforText: String = ""
    var body: some View {
        Form {
            if let currentInput = vm.currentExecutionItem {
                Text("Current: \(currentInput.title)")
                Text("Type: \(currentInput.inputType)")
                Text("Previous Input: \(currentInput.previousInput?.title ?? "")")
                Text("Next Input: \(currentInput.nextInput?.title ?? "")")
                
                if currentInput.inputType == "AskForTextInput" {
                    TextField("Enter Text here", text: $askforText)
                }
                
                if let nextInputItem = currentInput.nextInput {
                    Button(action: {
                        vm.showingInputExecutionSheet.toggle()
                        vm.recursiveNextInput(input: nextInputItem)
                    }, label: {
                        Text("Next: \(nextInputItem.title)")
                    })
                } else if currentInput.nextInput == nil {
                    Button(action: {
                        vm.showingInputExecutionSheet.toggle()
                    }, label: {
                        Text("Done")
                    })
                    
                }
                
            }
        }
    }
}

//struct ExecutingInputView_Previews: PreviewProvider {
//    static var previews: some View {
//        ExecutingInputView()
//    }
//}
