//
//  ExecuteVM.swift
//  BeingAnalytics
//
//  Created by Zachary Sturman on 9/1/23.
//

import Foundation
import SwiftUI

class ExecuteVM: ObservableObject {
    
    var dataService: DataService
    @Published var execution: TempExecution
    var currentInputExecutionVM: InputExecutionVM?
    private var currentInputID: UUID?
    private var executeID: UUID?
    private var triggerID: UUID?
    
    var outputString: String?
    
    @Binding var showingInputSheet: Bool
    
    var allInputsExecuted = false
    
    
    // EDIT EXISTING EXECUTION
    init(executeID: UUID, dataService: DataService, showingInputSheet: Binding<Bool>, outputString: String? = nil) {
           print("[ExecuteVM - Init (Existing Execution)] Initializing with existing execution ID.")
           self.dataService = dataService
           self._showingInputSheet = showingInputSheet
        self.outputString = outputString
        if let executionData = self.dataService.fetchObjectByID(by: executeID, entityType: Execution.self),
              let convertedExecution = self.dataService.convertExecutionToTempExecution(execution: executionData) {
               self.execution = convertedExecution
           } else {
               print("Error: Failed to fetch or convert execution data. Using default TempExecution.")
               self.execution = TempExecution()
           }
       }
       
       // NEW EXECUTION
    init(triggerID: UUID, dataService: DataService, showingInputSheet: Binding<Bool>, outputString: String? = nil) {
        print("[ExecuteVM - Init (New Execution)] Initializing with new trigger ID.")
        self.dataService = dataService
        self._showingInputSheet = showingInputSheet
        self.outputString = outputString
        self.execution = TempExecution()
        firstTriggerInput(triggerID: triggerID)
       }
       
    // GET THE FIRST INPUT OF THE TRIGGER
    func firstTriggerInput(triggerID: UUID) {
        // Fetch the trigger using the DataService
        if let trigger = dataService.fetchObjectByID(by: triggerID, entityType: Trigger.self) {
            currentInputID = trigger.firstInputID
            if let unwrappedActionStateID = trigger.actionState?.id {
                execution.actionStateID = unwrappedActionStateID
            }
            startInputExecution()
        } else {
            let newExecution = dataService.convertTempExecutionToCoreData(tempExecutionData: execution)
            _ = dataService.saveNewExecution(execution: newExecution)
        }
    }


    
    func startInputExecution() {
        guard let inputID = currentInputID else {
            print("[ExecuteVM] Error: currentInputID is nil.")
            return
        }
        currentInputExecutionVM = InputExecutionVM(inputID: inputID, dataService: dataService, execution: execution)
        if currentInputExecutionVM?.userActionRequired == true {
            showInputSheet()
        } else {
            hideInputSheet()
        }
        updateCalculations()
        checkInputExecution()
    }
    
    func updateCalculations() {
        if let inputExecutionVM = currentInputExecutionVM {
            if inputExecutionVM.calculationInputExecutions.isEmpty {
                return
            } else {
                execution.inputCalculations.append(contentsOf: inputExecutionVM.calculationInputExecutions)
            }
        }
    }
    
    func checkInputExecution() {
        // Check if the input execution is finalized
        if let inputExecutionVM = currentInputExecutionVM, inputExecutionFinalized(newInputExecution: inputExecutionVM) {
            
            if allInputsExecuted == true {
                return
            } else {
                appendInputExecutionToExecution(inputExecutionVM: inputExecutionVM)
            }
            if currentInputID != nil {
                startInputExecution()
            } else {
                finalizeExecution()
            }
        } else {
            showInputSheet()
        }
    }
    
    func finalizeExecution() {
        let newExecution = dataService.convertTempExecutionToCoreData(tempExecutionData: execution)
        _ = dataService.saveNewExecution(execution: newExecution)
        allInputsExecuted = true
        return
    }
    
    func appendInputExecutionToExecution(inputExecutionVM: InputExecutionVM) {
        execution.inputExecutions.append(inputExecutionVM.inputExecution)
        currentInputID = inputExecutionVM.nextInput
    }
    
    
    
    func inputExecutionFinalized(newInputExecution: InputExecutionVM) -> Bool {
        return newInputExecution.currentFinalized
    }
    
    func finalizeInput() {
        if let vm = currentInputExecutionVM {
            vm.inputIsFinalized()
            hideInputSheet()
            currentInputID = currentInputExecutionVM?.nextInput
            checkInputExecution()
            if currentInputExecutionVM?.userActionRequired == true {
                print("Yes User Required")
            } else {
                print("No User Required")
            }
        }

    }
    
    func showInputSheet() {
        if currentInputExecutionVM?.userActionRequired == true {
            showingInputSheet = true
        } else {
            showingInputSheet = false
        }
    }

    
    func hideInputSheet() {
        showingInputSheet = false
    }

}
