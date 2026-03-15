//
//  ActionStateExecutionVM.swift
//  BeingAnalytics
//
//  Created by Zachary Sturman on 9/9/23.
//

import SwiftUI
import Combine

class ActionStateExecutionVM: ObservableObject {
    var dataService: DataService
    
    // The current execution state
    @Published var currentExecution: TempExecution?
    
    var executionVM: ExecuteVM?
    
    var currentInput: Input?
    var askForTextInput: InputAskForText?
    var askForNumberInput: InputAskForNumber?
    
    @Published var showingInputSheet: Bool = false
    @Published var inputFinalized: Bool = false
    @Published var outputString: String = ""
    @Published var outputNumber: Double = 0.0
    
    
    init(dataService: DataService) {
        self.dataService = dataService
    }

    
    // Method to start the execution process
    func startExecution(triggerID: UUID) {
        executionVM = ExecuteVM(triggerID: triggerID, dataService: dataService, showingInputSheet: self.isInputSheetPresented, outputString: outputString)
        if let initialInput = executionVM?.currentInputExecutionVM?.currentInput {
            updateCurrentInput(newInput: initialInput)
            if let inputAsText = initialInput as? InputAskForText {
                self.askForTextInput = inputAsText
            }
        }
    }
    
    func updateCurrentInput(newInput: Input?) {
        self.currentInput = newInput
        self.askForTextInput = currentInput as? InputAskForText ?? nil
        self.askForNumberInput = currentInput as? InputAskForNumber ?? nil
        
        if askForTextInput != nil {
            if askForTextInput?.defaultBool == true {
                self.outputString = askForTextInput?.defaultString ?? ""
            } else {
                self.outputString = ""
            }
        } else {
            self.outputString = ""
        }
        
        if askForNumberInput != nil {
            self.outputNumber = askForNumberInput?.defaultValue ?? 0.0
        }
    }

    
    // Method to finalize input
    func finalizeInput() {
        // First try to finalize input using ExecuteVM
        if let vm = executionVM {
            if vm.currentInputExecutionVM?.inputExecution.inputExecutionEntityName == .InputExecutionString {
                vm.currentInputExecutionVM?.inputExecution.outputValueString = outputString
            } else if vm.currentInputExecutionVM?.inputExecution.inputExecutionEntityName == .InputExecutionNumber {
                vm.currentInputExecutionVM?.inputExecution.outputValueNumber = outputNumber
            }
            
            vm.finalizeInput()
            if vm.allInputsExecuted == false {
                resetInputValues()
                currentInput = vm.currentInputExecutionVM?.currentInput
                if let inputAsText = currentInput as? InputAskForText {
                    self.askForTextInput = inputAsText
                } else if let inputAskForNumber = currentInput as? InputAskForNumber {
                    self.askForNumberInput = inputAskForNumber
                }
            }
            return
        }
    }
    
    
    func resetInputValues() {
        self.currentInput = nil
        self.askForTextInput = nil
        self.askForNumberInput = nil

        
        self.showingInputSheet = false
        self.inputFinalized = false
        self.outputString = ""
        self.outputNumber = 0.0
    }
    
    
    func resetExecutionValues() {
        resetInputValues()
        self.currentExecution = nil
        self.executionVM = nil
    }

    
}

extension ActionStateExecutionVM {
    var isInputSheetPresented: Binding<Bool> {
        Binding(
            get: { self.showingInputSheet },
            set: { self.showingInputSheet = $0 }
        )
    }
}
