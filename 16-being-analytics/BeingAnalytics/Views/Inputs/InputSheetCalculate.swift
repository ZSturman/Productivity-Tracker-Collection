//
//  InputSheetCalculate.swift
//  BeingAnalytics
//
//  Created by Zachary Sturman on 9/14/23.
// 

import SwiftUI


// MARK: - InputSheetCalculate
struct InputSheetCalculate: View {
    
    // MARK: Properties
    @Environment(\.dismiss) private var dismiss
    @ObservedObject var vm: CreateActionStateVM
    @Binding var showCalculationSheet: Bool
    @Binding var shouldDismissParent: Bool
    
    @Binding var tempCalculate: TempInput
    
    var isEditing: Bool = false

    let calculationTypes = CalculationType.allCases
    let numberTypes = NumberType.allCases


    // MARK: Body
    var body: some View {
        NavigationStack {
            Form {
                Section {
                    Picker("Select type", selection: $tempCalculate.calculationType) {
                        ForEach(calculationTypes, id: \.self) { type in
                            Text(type.rawValue.capitalized).tag(type)
                        }
                    }
                    .pickerStyle(.segmented)
                }
                Section {
                    switch tempCalculate.calculationType {
                    case .number:
                        NumberCalculation(vm: vm, tempCalculate: $tempCalculate)
                    case .datetime:
                        DateCalculation(vm: vm, tempCalculate: $tempCalculate)
                    }
                }
                
                
                // OUTPUT
                Section {
                    switch tempCalculate.calculationType {
                    case .number:
                        HStack {
                            Picker("Output", selection: $tempCalculate.calculationOutputType) {
                                ForEach(numberTypes, id: \.self) { type in
                                    Text(type.rawValue.capitalized).tag(type)
                                }
                            }
                            .pickerStyle(.segmented)
                        }
                        HStack {
                            Spacer()
                            Text(formatNumberBasedOnType(type: tempCalculate.calculationOutputType, value: tempCalculate.numberValue))
                        }

                    case .datetime:
                        Text(FormattingHelper.shortenDateWithYear(tempCalculate.datetimeValue))
                    }
                }
            }
            
            .toolbar {
                ToolbarItem(placement: .navigationBarLeading) {
                    Button("Cancel") {
                        dismiss()
                    }
                }
                ToolbarItem(placement: .navigationBarTrailing) {
                    Button("Done") {
                        if isEditing == false {
                            vm.addInput(selectedInput: .calculate, tempCalculate: tempCalculate)
                        }
                        showCalculationSheet = false
                        shouldDismissParent = true
                    }

                    

                }
            }
        }
    }
    
    
    func formatNumberBasedOnType(type: NumberType, value: Double) -> String {
        switch type {
        case .integer:
            return FormattingHelper.formatNumber(value)
        case .decimal:
            return String(value)
        case .currency:
            return FormattingHelper.formatAsCurrency(value)
        }
    }

    
}

// MARK: - NumberCalculation
struct NumberCalculation: View {
    @ObservedObject var vm: CreateActionStateVM
    @Binding var tempCalculate: TempInput
    let calculationOperations = Operation.allCases
    @State var selectedInputOne: TempInput? = nil
    @State var selectedInputTwo: TempInput? = nil
    
    
    // MARK: Body
    var body: some View {
        VStack {
            HStack {
                Picker(selection: $selectedInputOne, label: Text("Select Input")) {
                    Text("Number").tag(nil as TempInput?)
                    ForEach(filterNumberCalculationInputs(), id: \.id) { input in
                        Text("\(input.order): \(input.title)").tag(input as TempInput?)
                    }
                }
            }
            
            HStack {
                if selectedInputOne == nil {
                    HStack {
                        Image(systemName: "number.square.fill")
                            .foregroundColor(.gray)
                            .font(.headline)
                        Spacer()
                        TextField("##", value: $tempCalculate.valueOne, formatter: NumberFormatter.custom)
                            .keyboardType(.numbersAndPunctuation)
                            .multilineTextAlignment(.trailing)
                            .onChange(of: tempCalculate.valueOne) { newValue in
                                if ((newValue?.isNaN) == nil) {
                                    tempCalculate.valueOne = 0 // default value or any fallback value
                                }
                            }

                        
                    }
                   
                } else {
                    HStack {
                        Image(systemName: "number.square.fill")
                            .foregroundColor(.gray)
                            .font(.headline)
                        Spacer()
                        Text(FormattingHelper.formatNumber(selectedInputOne?.numberValue ?? 0.0))
                            .foregroundColor(.gray)
                        
                    }
                }
            }
            .padding()
            .overlay(RoundedRectangle(cornerRadius: 10).stroke(Color.gray, lineWidth: 1))
            .background(Color.white)
            .onChange(of: selectedInputOne) { input in
                if input?.inputType == .setNumber || input?.inputType == .calculate {
                    tempCalculate.valueOne = input?.numberValue ?? 0.0
                } else if input?.inputType == .askForNumber {
                    tempCalculate.valueOne = input?.defaultNumberValue ?? 20
                } else {
                    tempCalculate.valueOne = 10
                }
            }

            


            
            HStack {
                
                Picker("Select operation", selection: $tempCalculate.calculateOperation) {
                    ForEach(calculationOperations, id: \.self) { operation in
                        Text(operation.rawValue).tag(operation)
                    }
                }
                .pickerStyle(.segmented)
            }
            
            HStack {
                Picker(selection: $selectedInputTwo, label: Text("Select Input")) {
                    Text("Number").tag(nil as TempInput?)
                    ForEach(filterNumberCalculationInputs(), id: \.id) { input in
                        Text("\(input.order)-\(input.title)").tag(input as TempInput?)
                    }
                }
            }
            

            
            HStack {
                if selectedInputTwo == nil {
                    HStack {
                        Image(systemName: "number.square.fill")
                            .foregroundColor(.gray)
                            .font(.headline)
                        Spacer()
                        TextField("##", value: $tempCalculate.valueTwo, formatter: NumberFormatter.custom)
                            .keyboardType(.numbersAndPunctuation)
                            .multilineTextAlignment(.trailing)
                            .onChange(of: tempCalculate.valueTwo) { newValue in
                                if ((newValue?.isNaN) == nil) {
                                    tempCalculate.valueTwo = 0 // default value or any fallback value
                                }
                            }

                    }
                } else {
                    HStack {
                        Image(systemName: "number.square.fill")
                            .foregroundColor(.gray)
                            .font(.headline)
                        Spacer()
                        Text(FormattingHelper.formatNumber(selectedInputTwo?.numberValue ?? 0.0))
                            .foregroundColor(.gray)
                    }
                }
            }
            .padding()
            .overlay(RoundedRectangle(cornerRadius: 10).stroke(Color.gray, lineWidth: 1))
            .background(Color.white)
            .onChange(of: selectedInputTwo) { input in
                if input?.inputType == .setNumber || input?.inputType == .calculate {
                    tempCalculate.valueTwo = input?.numberValue ?? 20
                } else if input?.inputType == .askForNumber {
                    tempCalculate.valueTwo = input?.defaultNumberValue ?? 10
                } else {
                    tempCalculate.valueTwo = 20
                }

            }

        
        }
        .onChange(of: tempCalculate.valueOne) { _ in
            tempCalculate.selectedInputOne = selectedInputOne?.id
            performCalculation()
        }
        .onChange(of: tempCalculate.valueTwo) { _ in
            tempCalculate.selectedInputTwo = selectedInputTwo?.id
            performCalculation()
        }
        .onChange(of: tempCalculate.calculateOperation) { _ in
            performCalculation()
        }
        .onAppear() {
            selectedInputOne = findInputById(tempCalculate.selectedInputOne)
            selectedInputTwo = findInputById(tempCalculate.selectedInputTwo)
            performCalculation()
        }

    }
    // MARK: Helper Functions
    func filterNumberCalculationInputs() -> [TempInput] {
        
        return (vm.selectedTrigger?.inputs ?? []).filter {
            $0.inputType.numberCalculation == true && $0.order <= tempCalculate.order && $0.id != tempCalculate.id
        }
    }
    
    
    func findInputById(_ id: UUID?) -> TempInput? {
        return vm.selectedTrigger?.inputs.first(where: { $0.id == id })
    }


    
    

    
    func performCalculation() {
        // Safely unwrap or use default value of 10
        let valueOne = tempCalculate.valueOne ?? 20
        let valueTwo = tempCalculate.valueTwo ?? 10
        
        if valueOne.isNaN || valueTwo.isNaN {
            print("Error: One of the values is NaN!")
            return
        }
        

        // Print for debugging
        print("Performing calculation with valueOne: \(valueOne) and valueTwo: \(valueTwo)")

        switch tempCalculate.calculateOperation {
        case .addition:
            tempCalculate.numberValue = valueOne + valueTwo
        case .subtraction:
            tempCalculate.numberValue = valueOne - valueTwo
        case .multiplication:
            tempCalculate.numberValue = valueOne * valueTwo
        case .division:
            if valueTwo != 0 {
                tempCalculate.numberValue = valueOne / valueTwo
            } else {
                tempCalculate.numberValue = 0
            }
        }

        // Round to nearest cent if currency is selected
        if tempCalculate.calculationOutputType == .currency {
            tempCalculate.numberValue = (tempCalculate.numberValue * 100).rounded() / 100
        }
        
        print("Resulting numberValue: \(tempCalculate.numberValue)")

    }




}


// MARK: - DateCalculation
struct DateCalculation: View {
    @ObservedObject var vm: CreateActionStateVM
    @Binding var tempCalculate: TempInput
    
    let dateOrTimeOptions = DateOrTime.allCases
    let calculationOperations = Operation.allCases

    // MARK: Body
    var body: some View {
        VStack {
            Picker("Select Date or Time", selection: $tempCalculate.calculationDateOrTime) {
                ForEach(dateOrTimeOptions, id: \.self) { option in
                    Text(option.rawValue.capitalized).tag(option)
                }
            }
            
            displayTriggerInputs()
            
            displayDatePicker()
            
            Picker("Select operation", selection: $tempCalculate.calculateOperation) {
                ForEach(calculationOperations, id: \.self) { operation in
                    Text(operation.rawValue).tag(operation)
                }
            }
        }
    }
    
    // MARK: Helper Functions
    func displayTriggerInputs() -> some View {
        ForEach(vm.selectedTrigger?.inputs ?? []){ input in
            if input.inputType.dateCalculation == true {
                Text("\(input.title) + \(input.order)")
                Text("\(input.inputOutput)")
            }
        }
    }
    
    func displayDatePicker() -> some View {
        switch tempCalculate.calculationDateOrTime {
        case .date:
            return DatePicker("Select Date", selection: $tempCalculate.datetimeValue, displayedComponents: [.date])
        case .time:
            return DatePicker("Select Time", selection: $tempCalculate.datetimeValue, displayedComponents: [.hourAndMinute])
        case .both:
            return DatePicker("Select Time", selection: $tempCalculate.datetimeValue)
        }
    }
}

extension NumberFormatter {
    static var currency: NumberFormatter {
        let formatter = NumberFormatter()
        formatter.numberStyle = .currency
        formatter.locale = .current
        return formatter
    }
}

extension NumberFormatter {
    static var custom: NumberFormatter {
        let formatter = NumberFormatter()
        formatter.allowsFloats = true
        formatter.minimumFractionDigits = 0
        formatter.maximumFractionDigits = 16
        return formatter
    }
}




