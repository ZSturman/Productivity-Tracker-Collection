//
//  ExecutionInputView.swift
//  ActionStateExecution
//
//  Created by Zachary Sturman on 8/2/23.
//
import SwiftUI

struct ExecutionInputView: View {
    @ObservedObject var executionViewModel: ExecutionViewModel
    @State private var inputValue: String = ""
    @State private var selectedOption: String = ""
    @State private var toggleState = true
    @State private var dateSelection = Date()
    @State private var stepperValue: Int = 0



    init(viewModel: ExecutionViewModel) {
        self.executionViewModel = viewModel
    }

    var body: some View {
        VStack {
            if let currentField = executionViewModel.currentField {
                Text(currentField.fieldName ?? "Unnamed Field")
                    .font(.title)
                    .padding()
                Text("\(String(currentField.order))")
                
                if executionViewModel.isTextField {
                    TextField("Enter Value", text: $inputValue)
                        .padding()
                        .background(Color.gray.opacity(0.2))
                        .cornerRadius(10)
                        .padding()
                } else if executionViewModel.isListView {
                    Picker(selection: $selectedOption, label: Text("Please choose")) {
                        ForEach(executionViewModel.listOptions, id: \.self) { option in
                            Text(option)
                        }
                    }
                    .padding()
                } else if executionViewModel.isCountField {
                    Stepper("Enter Count: \(inputValue)", value: $stepperValue)
                        .padding()

                } else if executionViewModel.isNumebrField {
                    TextField("Enter Number", text: $inputValue)
                        .keyboardType(.decimalPad)
                        .padding()
                        .background(Color.gray.opacity(0.2))
                        .cornerRadius(10)
                        .padding()
                } else if executionViewModel.isBoolField {
                    Toggle(isOn: $toggleState) {
                        Text("Toggle Value")
                    }
                    .padding()
                } else if executionViewModel.isDateTimeField {
                    DatePicker("Select Date", selection: $dateSelection)
                        .padding()
                } else if executionViewModel.isLocationField {
                    // Not sure about your location implementation, so I leave a placeholder here
                    Text("Location Field")
                } else if executionViewModel.isUploadField {
                    // Not sure about your upload field implementation, so I leave a placeholder here
                    Text("Upload Field")
                } else if executionViewModel.isCaptureField {
                    // Not sure about your capture field implementation, so I leave a placeholder here
                    Text("Capture Field")
                } else if executionViewModel.isOtherField {
                    // Not sure about your other field implementation, so I leave a placeholder here
                    Text("Other Field")
                }
                
            } else {
                Text("No Field Selected")
                    .font(.title)
                    .padding()
            }

            Button(action: {
                // Process the next field when button is clicked
                executionViewModel.processNextField(inputValue: inputValue)
                inputValue = ""
            }) {
                Text("Next")
                    .font(.headline)
                    .foregroundColor(.white)
                    .padding()
                    .background(Color.green)
                    .cornerRadius(10)
            }

            Button(action: {
                // Close the sheet when button is clicked
                executionViewModel.isSheetShowing = false
            }) {
                Text("Close")
                    .font(.headline)
                    .foregroundColor(.white)
                    .padding()
                    .background(Color.red)
                    .cornerRadius(10)
            }
        }
    }
}
