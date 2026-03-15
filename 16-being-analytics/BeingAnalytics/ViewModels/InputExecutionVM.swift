//
//  InputExecutionVM.swift
//  BeingAnalytics
//
//  Created by Zachary Sturman on 9/2/23.
//
 
import Foundation
import SwiftUI
 
class InputExecutionVM: ObservableObject {
    
    var dataService: DataService
    var execution: TempExecution
    @Published var inputExecution: TempInputExecution
    @Published var currentInput: Input
    
    var calculationInputExecutions: [TempInputCalculationExecution] = []
    
    var currentFinalized = false
    var nextInput: UUID? = nil
    
    @Published var userActionRequired = false
    
    init(inputID: UUID, dataService: DataService, execution: TempExecution) {
        self.dataService = dataService
        self.execution = execution
        
        // Ensure currentInput is initialized
        guard let fetchedInput = dataService.fetchObjectByID(by: inputID, entityType: Input.self) else {
            fatalError("Unable to fetch input with provided ID \(inputID)")
        }
        
        self.currentInput = fetchedInput
        self.nextInput = fetchedInput.nextInput?.id
        
        self.inputExecution = TempInputExecution(id: UUID(), inputExecutionType: .InputExecutionString)
        self.inputExecution.inputID = inputID
        self.currentFinalized = false
        print(execution.inputCalculations)
        checkAndCreateInputExecutions()
        getInputType()
        checkInputParams()
    }
    
    func inputIsFinalized() {
        print("Set to Finalized")
        currentFinalized = true
    }

    
    func checkAndCreateInputExecutions() {
        if currentInput.calculationInputOne?.count ?? 0 > 0 {
            for input in currentInput.calculationInputOne ?? [] {
                if let calulateInput = input as? InputCalculate {
                    let inputId = calulateInput.id
                    let newCalculationExecution = TempInputCalculationExecution(calculateInputID: inputId, valueOneInputExecution: inputExecution.id)
                    calculationInputExecutions.append(newCalculationExecution)
                }
            }
        }
        if currentInput.calculationInputTwo?.count ?? 0 > 0 {
            for input in currentInput.calculationInputTwo ?? [] {
                if let calulateInput = input as? InputCalculate {
                    let inputId = calulateInput.id
                    let newCalculationExecution = TempInputCalculationExecution(calculateInputID: inputId, valueTwoInputExecution: inputExecution.id)
                    calculationInputExecutions.append(newCalculationExecution)
                }
            }
        }
    }

    
    func checkInputParams() {
        
        switch currentInput.userActionRequired {
        case true:
            self.userActionRequired = true
        case false:
            self.userActionRequired = false
            
            if let _ = currentInput as? InputGetLocation {
                inputExecution.latitude = 1234567890
                inputExecution.longitude = 0987654321
            } else if let datetimeInput = currentInput as? InputCurrentDatetime {
                if datetimeInput.date == true && datetimeInput.time == true {
                    inputExecution.outputValueDatetime = Date()
                } else if datetimeInput.date == true && datetimeInput.time == false {
                    inputExecution.outputValueDatetime = Date()
                } else if datetimeInput.date == false && datetimeInput.time == true {
                    inputExecution.outputValueDatetime = Date()
                }
            } else if let setText = currentInput as? InputSetText {
                inputExecution.outputValueString = setText.setValue
            } else if let setNumber = currentInput as? InputSetNumber {
                inputExecution.outputValueNumber = setNumber.setValue
            } else if let calculate = currentInput as? InputCalculate {
//                if calculate.calculationType == "Number" {
//                    print("This is going to have the executionInput entity of InputExecutionNumber")
//                } else {
//                    print("This is going to have the executionInput entity of InputExecutionDatetime")
//                }
                runCalculationInput(input: calculate)
            } else {
                print("[InputExecutionVM - checkInputParams - unknown input")
            }
            
            inputIsFinalized()
        }
    }
    
    func runCalculationInput(input: InputCalculate) {
        
        if input.valueOneIsInput == true {
            if execution.inputCalculations.count > 0 {
                for inputCalculation in execution.inputCalculations {
                    if let unwrappedCalculateInputID = inputCalculation.calculateInputID, unwrappedCalculateInputID == input.id {
                        if inputCalculation.valueOneInputExecution != nil {
                            for previousInputExecution in execution.inputExecutions {
                                if previousInputExecution.id == inputCalculation.valueOneInputExecution {
                                    if previousInputExecution.inputExecutionEntityName == .InputExecutionNumber {
                                        inputExecution.valueOne = previousInputExecution.outputValueNumber
                                    }
                                }
                            }
                        } else {
                            inputExecution.valueOne = input.valueOne
                        }
                    }
                }
            }
        } else {
            inputExecution.valueOne = input.valueOne
        }
        
        if input.valueTwoIsInput == true {
            if execution.inputCalculations.count > 0 {
                for inputCalculation in execution.inputCalculations {
                    if let unwrappedCalculateInputID = inputCalculation.calculateInputID, unwrappedCalculateInputID == input.id {
                        if inputCalculation.valueTwoInputExecution != nil {
                            for previousInputExecution in execution.inputExecutions {
                                if previousInputExecution.id == inputCalculation.valueTwoInputExecution {
                                    if previousInputExecution.inputExecutionEntityName == .InputExecutionNumber {
                                        inputExecution.valueTwo = previousInputExecution.outputValueNumber
                                    }
                                }
                            }
                        } else {
                            inputExecution.valueTwo = input.valueTwo
                        }
                    }
                }
            }
        } else {
            inputExecution.valueTwo = input.valueTwo
        }
        

        
        if input.calculationType == "Datetime" {
            if input.calculationDateOrTime == "Date" {
                print("[InputExecution.runCalculationInput] JUST DATE")
                inputExecution.outputValueDatetime = Date()
            } else if input.calculationDateOrTime == "Time" {
                print("[InputExecution.runCalculationInput] JUST TIME")
                inputExecution.outputValueDatetime = Date()
            } else if input.calculationDateOrTime == "Both" {
                print("[InputExecution.runCalculationInput] BOTH")
                inputExecution.outputValueDatetime = Date()
            }
            
        } else if input.calculationType == "Number" {
            let operation = input.calculateOperation
            
            let valOne = inputExecution.valueOne ?? 0
            let valTwo = inputExecution.valueTwo ?? 0
            var calculationOutput: Double = 0
            
            switch operation {
            case "+":
                calculationOutput = valOne + valTwo
            case "-":
                calculationOutput = valOne - valTwo
            case "x":
                calculationOutput = valOne * valTwo
            case "/":
                if valTwo != 0 {
                    calculationOutput = valOne / valTwo
                } else {
                    calculationOutput = 0
                }
            default:
                calculationOutput = valOne + valTwo
            }
            
            
            if input.calculationOutputType == "Integer" {
                let intValue = Int(calculationOutput)
                inputExecution.outputValueNumber = Double(intValue)
            } else if input.calculationOutputType == "Decimal" {
                inputExecution.outputValueNumber = calculationOutput
            } else if input.calculationOutputType == "Currency" {
                let currencyValue = (calculationOutput * 100).rounded() / 100
                inputExecution.outputValueNumber = currencyValue
            }
        }
    }

    
    
    
    
    
    func getInputType() {
        if currentInput is InputAskForNumber || currentInput is InputSetNumber {
            inputExecution.inputExecutionEntityName = .InputExecutionNumber
        } else if currentInput is InputAskForText || currentInput is InputSetText {
            inputExecution.inputExecutionEntityName = .InputExecutionString
        } else if currentInput is InputCurrentDatetime {
            inputExecution.inputExecutionEntityName = .InputExecutionDatetime
        } else if currentInput is InputGetLocation {
            inputExecution.inputExecutionEntityName = .InputExecutionLocation
        } else if let calculateInput = currentInput as? InputCalculate {
            if calculateInput.calculationType == "Number" {
                inputExecution.inputExecutionEntityName = .InputExecutionNumber
            } else if calculateInput.calculationType == "Datetime" {
                inputExecution.inputExecutionEntityName = .InputExecutionDatetime
            }
        } else {
            print("[InputExecutionVM - getInputType] Warning: Input is of an unknown type.")
        }
    }

    


}
